import importlib.util
import io
import json
import os
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

SCRIPT = Path(__file__).with_name("run_benchmark.py")
SPEC = importlib.util.spec_from_file_location("run_benchmark", SCRIPT)
RUN = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RUN)

ASSERTIONS = [{
    "kind": "required_patterns",
    "text": "The response contains its required marker.",
    "patterns": ["response"],
}]


class RunBenchmarkTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.bin = self.root / "bin"
        self.bin.mkdir()
        self.harness = self.bin / "fake-harness"
        self.harness.write_text(
            "#!/usr/bin/env python3\n"
            "import json, os, pathlib, sys\n"
            "log = os.environ.get('CALL_LOG')\n"
            "if log:\n"
            " with open(log, 'a', encoding='utf-8') as stream: stream.write('call\\n')\n"
            "prompt = pathlib.Path(sys.argv[sys.argv.index('--prompt-file') + 1]).read_text()\n"
            "if prompt.strip() == 'Reply with exactly OK.': print('OK')\n"
            "else:\n"
            " print('This response has enough words for the output validity check and confirms that only declared input files are visible here now.')\n",
            encoding="utf-8",
        )
        self.harness.chmod(0o755)
        self.old_path = os.environ.get("PATH", "")
        os.environ["PATH"] = f"{self.bin}{os.pathsep}{self.old_path}"
        self.addCleanup(os.environ.__setitem__, "PATH", self.old_path)

    def write_json(self, path, value):
        path.write_text(json.dumps(value), encoding="utf-8")

    def run_cross_harness(self, args):
        return RUN.main(["--cross-harness", *args])

    def test_cross_harness_flag_is_required(self):
        status = RUN.main([
            "--workspace", str(self.root / "workspace"),
            "--iteration", "1",
            "--manifest", str(self.root / "missing-manifest.json"),
            "--routes", str(self.root / "missing-routes.json"),
            "--seed", "1",
        ])

        self.assertEqual(status, 1)
        self.assertFalse((self.root / "workspace").exists())

    def test_relative_input_root_and_named_arms(self):
        manifest_dir = self.root / "evals"
        inputs = manifest_dir / "v2-inputs" / "eval-1-sample"
        inputs.mkdir(parents=True)
        (inputs / "draft.md").write_text("input", encoding="utf-8")
        (manifest_dir / "rule.md").write_text("rule", encoding="utf-8")
        manifest = manifest_dir / "evals.json"
        self.write_json(manifest, {
            "schema_version": 2,
            "input_root": "v2-inputs",
            "arms": {"baseline": {}, "with_rule": {"artifact_path": "rule.md"}},
            "comparisons": [{"id": "rule", "primary": "with_rule", "baseline": "baseline"}],
            "evals": [{"id": 1, "name": "sample", "prompt": "Rewrite.", "files": ["draft.md"], "minimum_words": 10, "assertions": ASSERTIONS}],
        })
        routes = self.root / "routes.json"
        self.write_json(routes, {"routes": {"fake": {
            "binary": "fake-harness", "model": "model1m",
            "argv": ["--prompt-file", "{prompt_file}"],
            "system_argv": ["--artifact", "{artifact}"], "response": "text",
            "context_canary": "List visible artifact rules.",
            "forbidden_context_markers": ["SECRET_ARTIFACT"],
        }}})

        output = io.StringIO()
        with redirect_stdout(output):
            status = self.run_cross_harness([
                "--workspace", str(self.root / "workspace"), "--iteration", "2",
                "--manifest", str(manifest), "--routes", str(routes),
                "--repeats", "1", "--seed", "7",
            ])

        self.assertEqual(status, 0)
        self.assertIn("Progress: event=route-check-start check=preflight", output.getvalue())
        self.assertIn(
            "event=run-finish case=1 arm=baseline route=fake model=model1m repeat=1 state=valid",
            output.getvalue(),
        )
        result = self.root / "workspace" / "iteration-2" / "eval-1-sample" / "baseline@model" / "run-1" / "result.json"
        self.assertTrue(result.is_file())
        self.assertEqual(json.loads(result.read_text())["state"], "valid")
        run_manifest = json.loads((self.root / "workspace" / "iteration-2" / "manifest.json").read_text())
        self.assertEqual(set(run_manifest["arms"]), {"baseline", "with_rule"})
        self.assertEqual(run_manifest["input_root"], str((manifest_dir / "v2-inputs").resolve()))
        self.assertEqual(run_manifest["evals"][0]["resolved_files"], [{
            "path": str((inputs / "draft.md").resolve()),
            "sha256": RUN.artifact_digest(inputs / "draft.md"),
        }])
        self.assertEqual(run_manifest["arms"]["with_rule"]["artifact_path"], str((manifest_dir / "rule.md").resolve()))
        self.assertEqual(run_manifest["arms"]["with_rule"]["artifact_sha256"], RUN.artifact_digest(manifest_dir / "rule.md"))
        self.assertEqual(run_manifest["source_manifest"], str(manifest.resolve()))
        self.assertEqual(run_manifest["run_plan"]["routes"], [{"id": "fake", "model": "model1m"}])
        self.assertEqual(run_manifest["run_plan"]["registry_path"], str(routes.resolve()))
        self.assertEqual(run_manifest["run_plan"]["registry_sha256"], RUN.artifact_digest(routes))
        self.assertEqual(run_manifest["run_plan"]["repeats"], 1)
        self.assertEqual(run_manifest["run_plan"]["seed"], 7)

    def test_comparison_filter_runs_only_its_two_arms(self):
        manifest = self.root / "evals.json"
        self.write_json(manifest, {
            "schema_version": 2,
            "arms": {"baseline": {}, "with_rule": {}, "with_skill": {}},
            "comparisons": [
                {"id": "rule", "primary": "with_rule", "baseline": "baseline"},
                {"id": "skill", "primary": "with_skill", "baseline": "baseline"},
            ],
            "evals": [{"id": 1, "name": "sample", "prompt": "Rewrite.", "files": [], "assertions": ASSERTIONS}],
        })
        routes = self.root / "routes.json"
        self.write_json(routes, {"routes": {"fake": {
            "binary": "fake-harness", "model": "model",
            "argv": ["--prompt-file", "{prompt_file}"], "response": "text",
            "context_canary": "List visible artifact rules.",
            "forbidden_context_markers": ["SECRET_ARTIFACT"],
        }}})
        workspace = self.root / "workspace"

        status = self.run_cross_harness([
            "--workspace", str(workspace), "--iteration", "1",
            "--manifest", str(manifest), "--routes", str(routes),
            "--comparison", "skill", "--seed", "1",
        ])

        self.assertEqual(status, 0)
        run_root = workspace / "iteration-1"
        run_manifest = json.loads((run_root / "manifest.json").read_text())
        self.assertEqual(set(run_manifest["arms"]), {"baseline", "with_skill"})
        self.assertEqual([item["id"] for item in run_manifest["comparisons"]], ["skill"])
        self.assertTrue((run_root / "eval-1-sample" / "baseline@model" / "run-1" / "result.json").is_file())
        self.assertTrue((run_root / "eval-1-sample" / "with_skill@model" / "run-1" / "result.json").is_file())
        self.assertFalse((run_root / "eval-1-sample" / "with_rule@model").exists())

    def test_default_workspace_uses_environment_root_and_deck(self):
        os.environ["ROOT_BENCHMARK"] = str(self.root / "bench-root")
        self.addCleanup(os.environ.pop, "ROOT_BENCHMARK", None)

        with_deck = RUN.default_workspace({"artifact_name": "Rule", "deck": "runedeck"})
        without_deck = RUN.default_workspace({"artifact_name": "Rule"})

        self.assertEqual(with_deck, self.root / "bench-root" / "runedeck" / "Rule")
        self.assertEqual(without_deck, self.root / "bench-root" / "Rule")
        with self.assertRaisesRegex(ValueError, "artifact_name"):
            RUN.default_workspace({})
        for manifest in (
            {"artifact_name": "../outside"},
            {"artifact_name": "Rule", "deck": "../outside"},
        ):
            with self.subTest(manifest=manifest), self.assertRaisesRegex(
                ValueError, "safe path segment",
            ):
                RUN.default_workspace(manifest)

    def test_manifest_resources_cannot_escape_the_manifest_directory(self):
        manifest = self.root / "source" / "manifest.json"
        manifest.parent.mkdir()

        for value in ("../outside", str(self.root / "outside")):
            with self.subTest(value=value), self.assertRaises(ValueError):
                RUN.resolve_manifest_path(manifest, value, "input_root")

    def test_model_identifier_is_one_safe_directory_segment(self):
        target = RUN.result_dir(self.root, {"id": 1, "name": "case"}, "baseline", "proton-lumo/lumo-max", 1)

        self.assertEqual(target.parent.name, "baseline@proton-lumo%2Flumo-max")

    def test_display_model_removes_trailing_context_suffix(self):
        self.assertEqual(RUN.display_model("claude-opus-51m"), "claude-opus-5")
        self.assertEqual(RUN.display_model("claude-opus-5-1m"), "claude-opus-5")
        self.assertEqual(RUN.display_model("claude-opus-5[1m]"), "claude-opus-5")
        self.assertEqual(RUN.display_model("claude-opus-5"), "claude-opus-5")

    def test_artifact_digest_covers_directory_paths_and_contents(self):
        artifact = self.root / "Skill"
        artifact.mkdir()
        (artifact / "SKILL.md").write_text("# Skill\n", encoding="utf-8")
        first = RUN.artifact_digest(artifact)

        (artifact / "support.md").write_text("support\n", encoding="utf-8")
        second = RUN.artifact_digest(artifact)

        self.assertNotEqual(first, second)
        self.assertEqual(second, RUN.artifact_digest(artifact))

    def test_artifact_path_rejects_a_wrong_digest(self):
        artifact = self.root / "rule.md"
        artifact.write_text("rule\n", encoding="utf-8")
        manifest = self.root / "evals.json"

        with self.assertRaisesRegex(ValueError, "digest does not match"):
            RUN.artifact_path(manifest, {
                "artifact_kind": "rule",
                "artifact_path": "rule.md",
                "artifact_sha256": "0" * 64,
            })

    def test_existing_matrix_requires_a_new_iteration(self):
        manifest = self.root / "evals.json"
        self.write_json(manifest, {
            "schema_version": 2,
            "arms": {"baseline": {}},
            "comparisons": [],
            "evals": [{"id": 1, "name": "sample", "prompt": "Rewrite.", "assertions": ASSERTIONS}],
        })
        routes = self.root / "routes.json"
        self.write_json(routes, {"routes": {"fake": {
            "binary": "fake-harness", "model": "model",
            "argv": ["--prompt-file", "{prompt_file}"], "response": "text",
            "context_canary": "List visible artifact rules.",
            "forbidden_context_markers": ["SECRET_ARTIFACT"],
        }}})
        workspace = self.root / "workspace"
        (workspace / "iteration-1" / "eval-stale").mkdir(parents=True)
        call_log = self.root / "calls.log"
        os.environ["CALL_LOG"] = str(call_log)
        self.addCleanup(os.environ.pop, "CALL_LOG", None)

        status = self.run_cross_harness([
            "--workspace", str(workspace), "--iteration", "1",
            "--manifest", str(manifest), "--routes", str(routes), "--seed", "1",
        ])

        self.assertEqual(status, 1)
        self.assertFalse(call_log.exists())

    def test_json_response_keeps_resolved_identity(self):
        text, usage, route = RUN.parse_response(json.dumps({
            "text": "OK", "usage": {"output_tokens": 2},
            "resolved_model": "model", "resolved_binary": "/bin/provider",
        }), "json")

        self.assertEqual(text, "OK")
        self.assertEqual(usage["output_tokens"], 2)
        self.assertEqual(route["resolved_binary"], "/bin/provider")

    def test_jsonl_response_selects_the_last_message_id(self):
        stdout = (
            '{"type":"text","part":{"messageID":"msg_1","text":"I will read the file."}}\n'
            '{"type":"step_finish","part":{"messageID":"msg_1"}}\n'
            '{"type":"text","part":{"messageID":"msg_2","text":"Final "}}\n'
            '{"type":"text","part":{"messageID":"msg_2","text":"answer."}}'
        )

        text, _, _ = RUN.parse_response(stdout, "jsonl")

        self.assertEqual(text, "Final answer.")

    def test_jsonl_response_rejects_mixed_message_identity(self):
        stdout = (
            '{"type":"text","part":{"messageID":"msg_1","text":"Narration."}}\n'
            '{"type":"text","part":{"text":"Final answer."}}'
        )

        with self.assertRaisesRegex(ValueError, "mix identified and unidentified"):
            RUN.parse_response(stdout, "jsonl")

    def test_prompt_placeholder_keeps_literal_braces(self):
        self.assertEqual(
            RUN.expand("--prompt={prompt}", {"prompt": "Keep {literal} braces."}),
            "--prompt=Keep {literal} braces.",
        )

    def test_treatment_arm_requires_artifact_path(self):
        manifest = {
            "schema_version": 2,
            "arms": {"baseline": {}, "with_rule": {"artifact_kind": "rule"}},
            "comparisons": [{"id": "rule", "primary": "with_rule", "baseline": "baseline"}],
            "evals": [{"id": 1, "name": "sample", "prompt": "Review.", "assertions": ASSERTIONS}],
        }

        with self.assertRaisesRegex(ValueError, "needs artifact_path"):
            RUN.validate_manifest(manifest)

    def test_comparison_arms_must_differ(self):
        manifest = {
            "schema_version": 2,
            "arms": {"baseline": {}},
            "comparisons": [{"id": "same", "primary": "baseline", "baseline": "baseline"}],
            "evals": [{"id": 1, "name": "sample", "prompt": "Review.", "assertions": ASSERTIONS}],
        }

        with self.assertRaisesRegex(ValueError, "must differ"):
            RUN.validate_manifest(manifest)

    def test_comparison_ids_must_be_present_and_unique(self):
        manifest = {
            "schema_version": 2,
            "arms": {"baseline": {}, "with_rule": {}},
            "comparisons": [
                {"primary": "with_rule", "baseline": "baseline"},
            ],
            "evals": [{"id": 1, "name": "sample", "prompt": "Review.", "assertions": ASSERTIONS}],
        }

        with self.assertRaisesRegex(ValueError, "one safe path segment"):
            RUN.validate_manifest(manifest)

        manifest["comparisons"] = [
            {"id": "rule", "primary": "with_rule", "baseline": "baseline"},
            {"id": "rule", "primary": "with_rule", "baseline": "baseline"},
        ]
        with self.assertRaisesRegex(ValueError, "must be unique"):
            RUN.validate_manifest(manifest)

    def test_fixed_judging_configuration_is_valid(self):
        judging = {
            "dimensions": [
                {"id": "clarity", "label": "Clarity", "criterion": "Prefer clear text.", "weight": 1},
                {"id": "fluency", "label": "Fluency", "criterion": "Prefer natural text.", "weight": 0.5},
                {"id": "directness", "label": "Directness", "criterion": "Prefer direct text.", "weight": 1},
            ],
            "guards": ["Do not judge factual accuracy."],
        }

        RUN.validate_judging_config(judging, {"trade_off": 0.4, "win": 0.5})

    def test_invalid_judging_configuration_is_rejected(self):
        dimensions = [
            {"id": "clarity", "label": "Clarity", "criterion": "Prefer clear text.", "weight": 1},
            {"id": "fluency", "label": "Fluency", "criterion": "Prefer natural text.", "weight": 0.5},
            {"id": "directness", "label": "Directness", "criterion": "Prefer direct text.", "weight": 1},
        ]
        invalid = {
            "missing dimension": ({"dimensions": dimensions[:2]}, None),
            "duplicate dimension": ({"dimensions": [*dimensions[:2], dimensions[1]]}, None),
            "weight above one": ({
                "dimensions": [
                    {**dimensions[0], "weight": 1.1},
                    *dimensions[1:],
                ],
            }, None),
            "non-finite weight": ({
                "dimensions": [
                    {**dimensions[0], "weight": float("nan")},
                    *dimensions[1:],
                ],
            }, None),
            "threshold below zero": ({"dimensions": dimensions}, {"trade_off": -0.1}),
            "reversed thresholds": ({"dimensions": dimensions}, {"trade_off": 0.7, "win": 0.5}),
        }

        for name, (judging, thresholds) in invalid.items():
            with self.subTest(name=name), self.assertRaises((TypeError, ValueError)):
                RUN.validate_judging_config(judging, thresholds)

    def test_write_result_stores_raw_provider_output(self):
        target = self.root / "run-1"

        RUN.write_result(
            target,
            {
                "state": "valid",
                "response": "Parsed response.",
                "provider_output": '{"response":"Parsed response."}\n',
            },
            {"model": "test-model"},
        )

        self.assertEqual(
            (target / "outputs" / "provider-output.txt").read_text(),
            '{"response":"Parsed response."}\n',
        )
        self.assertNotIn("provider_output", json.loads((target / "result.json").read_text()))

    def test_write_result_rejects_nonfinite_json_numbers(self):
        with self.assertRaises(ValueError):
            RUN.write_result(
                self.root / "nonfinite-run",
                {"state": "valid", "usage": {"total_tokens": float("nan")}},
                {"model": "test-model"},
            )

    def test_prepend_treatment_combines_artifact_and_prompt(self):
        artifact = self.root / "rule.md"
        artifact.write_text("RULE TEXT", encoding="utf-8")

        combined = RUN.treatment_prompt("TASK TEXT", artifact, {"treatment_mode": "prepend"})

        self.assertEqual(combined, "RULE TEXT\n\nTASK TEXT")

    def test_native_artifact_arguments_keep_the_task_prompt_separate(self):
        artifact = self.root / "agent.md"
        artifact.write_text("AGENT TEXT", encoding="utf-8")

        combined = RUN.treatment_prompt(
            "TASK TEXT",
            artifact,
            {"artifact_argv": ["--agent", "{artifact}"]},
        )

        self.assertEqual(combined, "TASK TEXT")

    def test_skill_directory_stages_support_files_without_byte_changes(self):
        skill = self.root / "SimplifiedTechnicalEnglish"
        skill.mkdir()
        (skill / "SKILL.md").write_text("# Skill", encoding="utf-8")
        (skill / "asset.bin").write_bytes(b"\x00\xffartifact")
        scratch = self.root / "scratch"
        control = self.root / "control"
        scratch.mkdir()
        control.mkdir()

        context, staged = RUN.stage_artifact(skill, scratch, control)

        copied = scratch / ".bench-artifact" / skill.name
        self.assertEqual(staged, copied)
        self.assertEqual((copied / "asset.bin").read_bytes(), b"\x00\xffartifact")
        self.assertIn(f"Skill directory: {copied}", context.read_text())
        self.assertIn("# Skill", context.read_text())

    def test_file_artifact_is_staged_inside_scratch(self):
        artifact = self.root / "agent.md"
        artifact.write_text("AGENT", encoding="utf-8")
        scratch = self.root / "file-scratch"
        control = self.root / "file-control"
        scratch.mkdir()
        control.mkdir()

        context, staged = RUN.stage_artifact(artifact, scratch, control)

        self.assertEqual(context, staged)
        self.assertEqual(staged, scratch / ".bench-artifact" / "agent.md")
        self.assertEqual(staged.read_text(), "AGENT")

    def test_skill_directory_rejects_symbolic_links(self):
        skill = self.root / "LinkedSkill"
        skill.mkdir()
        (skill / "SKILL.md").write_text("# Skill", encoding="utf-8")
        (skill / "outside").symlink_to(self.root / "secret")
        scratch = self.root / "linked-scratch"
        control = self.root / "linked-control"
        scratch.mkdir()
        control.mkdir()

        with self.assertRaisesRegex(ValueError, "symbolic link"):
            RUN.stage_artifact(skill, scratch, control)

    def test_agent_rule_and_skill_matrix_stages_native_sources(self):
        harness = self.bin / "artifact-harness"
        harness.write_text(
            "#!/usr/bin/env python3\n"
            "import json, os, pathlib, sys\n"
            "prompt = pathlib.Path(sys.argv[sys.argv.index('--prompt-file') + 1]).read_text()\n"
            "artifact = sys.argv[sys.argv.index('--artifact') + 1] if '--artifact' in sys.argv else ''\n"
            "source = sys.argv[sys.argv.index('--artifact-source') + 1] if '--artifact-source' in sys.argv else ''\n"
            "record = {'cwd': str(pathlib.Path.cwd()), 'artifact': artifact, 'source': source}\n"
            "if source:\n"
            " path = pathlib.Path(source)\n"
            " record['source_name'] = path.name\n"
            " record['source_is_dir'] = path.is_dir()\n"
            " record['source_in_cwd'] = path.resolve().is_relative_to(pathlib.Path.cwd().resolve())\n"
            " record['support_exists'] = (path / 'support.txt').is_file() if path.is_dir() else False\n"
            "with open(os.environ['INSPECTION_LOG'], 'a', encoding='utf-8') as stream:\n"
            " stream.write(json.dumps(record) + '\\n')\n"
            "if prompt.strip() == 'Reply with exactly OK.': print('OK')\n"
            "elif prompt.strip() == 'List visible artifact rules.': print('No tested marker is visible.')\n"
            "else: print('This valid benchmark response contains enough words and proves the portable artifact harness completed its isolated test run.')\n",
            encoding="utf-8",
        )
        harness.chmod(0o755)
        manifest_dir = self.root / "portable"
        inputs = manifest_dir / "inputs" / "eval-1-sample"
        inputs.mkdir(parents=True)
        (inputs / "draft.md").write_text("input", encoding="utf-8")
        (manifest_dir / "agent.md").write_text("AGENT", encoding="utf-8")
        (manifest_dir / "rule.md").write_text("RULE", encoding="utf-8")
        skill = manifest_dir / "Skill"
        skill.mkdir()
        (skill / "SKILL.md").write_text("# Skill", encoding="utf-8")
        (skill / "support.txt").write_text("support", encoding="utf-8")
        manifest = manifest_dir / "evals.json"
        self.write_json(manifest, {
            "schema_version": 2,
            "input_root": "inputs",
            "arms": {
                "baseline": {},
                "with_agent": {"artifact_kind": "agent", "artifact_path": "agent.md"},
                "with_rule": {"artifact_kind": "rule", "artifact_path": "rule.md"},
                "with_skill": {"artifact_kind": "skill", "artifact_path": "Skill"},
            },
            "comparisons": [
                {"id": "agent", "primary": "with_agent", "baseline": "baseline"},
                {"id": "rule", "primary": "with_rule", "baseline": "baseline"},
                {"id": "skill", "primary": "with_skill", "baseline": "baseline"},
            ],
            "evals": [{
                "id": 1, "name": "sample", "prompt": "Review.",
                "files": ["draft.md"], "minimum_words": 10,
                "assertions": ASSERTIONS,
            }],
        })
        inspection_log = self.root / "inspection.jsonl"
        routes = self.root / "portable-routes.json"
        self.write_json(routes, {"routes": {"fake": {
            "binary": "artifact-harness", "model": "model",
            "argv": ["--prompt-file", "{prompt_file}"],
            "artifact_argv": ["--artifact", "{artifact}", "--artifact-source", "{artifact_source}"],
            "response": "text", "env": {"INSPECTION_LOG": str(inspection_log)},
            "context_canary": "List visible artifact rules.",
            "forbidden_context_markers": ["SECRET_ARTIFACT"],
        }}})

        status = self.run_cross_harness([
            "--workspace", str(self.root / "portable-workspace"), "--iteration", "1",
            "--manifest", str(manifest), "--routes", str(routes), "--seed", "9",
        ])

        self.assertEqual(status, 0)
        records = [json.loads(line) for line in inspection_log.read_text().splitlines()]
        treatments = [record for record in records if record["source"]]
        self.assertEqual({record["source_name"] for record in treatments}, {"agent.md", "rule.md", "Skill"})
        self.assertTrue(all(record["source_in_cwd"] for record in treatments))
        skill_record = next(record for record in treatments if record["source_name"] == "Skill")
        self.assertTrue(skill_record["source_is_dir"])
        self.assertTrue(skill_record["support_exists"])
        root = self.root / "portable-workspace" / "iteration-1" / "eval-1-sample"
        for arm in ("baseline", "with_agent", "with_rule", "with_skill"):
            result = json.loads((root / f"{arm}@model" / "run-1" / "result.json").read_text())
            self.assertEqual(result["state"], "valid")
            self.assertEqual(result["route"]["requested_route"], "fake")

    def test_explicit_input_dir_resolves_below_input_root(self):
        manifest_dir = self.root / "evals"
        inputs = manifest_dir / "v2-inputs" / "custom-case"
        inputs.mkdir(parents=True)
        (inputs / "draft.md").write_text("input", encoding="utf-8")
        manifest = manifest_dir / "evals.json"
        self.write_json(manifest, {
            "schema_version": 2, "input_root": "v2-inputs",
            "arms": {"baseline": {}}, "comparisons": [],
            "evals": [{"id": 1, "name": "sample", "input_dir": "custom-case", "prompt": "Rewrite.", "files": ["draft.md"], "minimum_words": 10, "assertions": ASSERTIONS}],
        })
        routes = self.root / "routes.json"
        self.write_json(routes, {"routes": {"fake": {
            "binary": "fake-harness", "model": "model", "argv": ["--prompt-file", "{prompt_file}"], "response": "text",
            "context_canary": "List visible artifact rules.",
            "forbidden_context_markers": ["SECRET_ARTIFACT"],
        }}})

        status = self.run_cross_harness(["--workspace", str(self.root / "workspace"), "--iteration", "1", "--manifest", str(manifest), "--routes", str(routes), "--seed", "1"])

        self.assertEqual(status, 0)

    def test_provider_failure_keeps_structured_details(self):
        failing = self.bin / "failing-harness"
        failing.write_text(
            "#!/usr/bin/env python3\n"
            "import json\n"
            "print(json.dumps({'ok': False, 'details': {'message': 'quota'}}))\n"
            "raise SystemExit(1)\n",
            encoding="utf-8",
        )
        failing.chmod(0o755)
        route = {"binary": "failing-harness", "model": "model", "response": "json"}

        result = RUN.invoke("failing", route, "prompt", None, [], 10)

        self.assertEqual(result["state"], "provider_failure")
        self.assertEqual(result["error"], {"message": "quota"})

    def test_non_object_provider_output_is_invalid(self):
        invalid = self.bin / "invalid-harness"
        invalid.write_text("#!/bin/sh\nprintf '[]\\n'\n", encoding="utf-8")
        invalid.chmod(0o755)
        route = {"binary": "invalid-harness", "model": "model", "response": "json"}

        result = RUN.invoke("invalid", route, "prompt", None, [], 10)

        self.assertEqual(result["state"], "invalid_output")
        self.assertEqual(result["provider_output"], "[]\n")
        self.assertEqual(result["error"], "provider output must contain a JSON object")

    def test_word_limits_belong_to_grading_not_execution_validity(self):
        result = {
            "state": "valid",
            "response": "Short answer.",
        }

        validated = RUN.validate_output(
            result,
            {"minimum_words": 100, "maximum_words": 200},
        )

        self.assertEqual(validated["state"], "valid")
        self.assertEqual(validated["word_count"], 2)

    def test_context_canary_blocks_forbidden_marker(self):
        leaking = self.bin / "leaking-harness"
        leaking.write_text(
            "#!/usr/bin/env python3\n"
            "import pathlib, sys\n"
            "prompt = pathlib.Path(sys.argv[sys.argv.index('--prompt-file') + 1]).read_text()\n"
            "print('OK' if prompt.strip() == 'Reply with exactly OK.' else 'ASD-STE100 is visible')\n",
            encoding="utf-8",
        )
        leaking.chmod(0o755)
        manifest = self.root / "evals.json"
        self.write_json(manifest, {
            "schema_version": 2, "arms": {"baseline": {}}, "comparisons": [],
            "evals": [{"id": 1, "name": "sample", "prompt": "Rewrite.", "files": [], "assertions": ASSERTIONS}],
        })
        routes = self.root / "routes.json"
        self.write_json(routes, {"routes": {"fake": {
            "binary": "leaking-harness", "model": "model",
            "argv": ["--prompt-file", "{prompt_file}"], "response": "text",
            "context_canary": "List visible writing rules.",
            "forbidden_context_markers": ["ASD-STE100"],
        }}})

        status = self.run_cross_harness([
            "--workspace", str(self.root / "workspace"), "--iteration", "1",
            "--manifest", str(manifest), "--routes", str(routes), "--seed", "1",
        ])

        self.assertEqual(status, 1)
        canaries = json.loads((self.root / "workspace" / "iteration-1" / "context-canaries.json").read_text())
        self.assertEqual(canaries["fake"]["state"], "context_failure")

    def test_routes_cannot_share_display_model(self):
        manifest = self.root / "evals.json"
        self.write_json(manifest, {
            "schema_version": 2, "arms": {"baseline": {}}, "comparisons": [],
            "evals": [{"id": 1, "name": "sample", "prompt": "Rewrite.", "files": [], "assertions": ASSERTIONS}],
        })
        route = {
            "binary": "fake-harness", "model": "model1m",
            "argv": ["--prompt-file", "{prompt_file}"], "response": "text",
            "context_canary": "List visible artifact rules.",
            "forbidden_context_markers": ["SECRET_ARTIFACT"],
        }
        routes = self.root / "routes.json"
        self.write_json(routes, {"routes": {"first": route, "second": route}})

        status = self.run_cross_harness([
            "--workspace", str(self.root / "workspace"), "--iteration", "1",
            "--manifest", str(manifest), "--routes", str(routes), "--seed", "1",
        ])

        self.assertEqual(status, 1)

    def test_large_matrix_approval_counts_route_checks(self):
        manifest = self.root / "evals.json"
        self.write_json(manifest, {
            "schema_version": 2, "arms": {str(index): {} for index in range(21)},
            "comparisons": [],
            "evals": [{"id": 1, "name": "sample", "prompt": "Rewrite.", "files": [], "assertions": ASSERTIONS}],
        })
        routes = self.root / "routes.json"
        call_log = self.root / "calls.log"
        self.write_json(routes, {"routes": {"fake": {
            "binary": "fake-harness", "model": "model", "argv": ["--prompt-file", "{prompt_file}"], "response": "text",
            "env": {"CALL_LOG": str(call_log)},
            "context_canary": "List visible artifact rules.",
            "forbidden_context_markers": ["SECRET_ARTIFACT"],
        }}})

        status = self.run_cross_harness([
            "--workspace", str(self.root / "workspace"), "--iteration", "1",
            "--manifest", str(manifest), "--routes", str(routes),
            "--seed", "1",
        ])

        self.assertEqual(status, 1)
        self.assertFalse(call_log.exists())

        status = self.run_cross_harness([
            "--workspace", str(self.root / "workspace"), "--iteration", "1",
            "--manifest", str(manifest), "--routes", str(routes),
            "--seed", "1", "--approve", "21",
        ])

        self.assertEqual(status, 1)
        self.assertFalse(call_log.exists())

        status = self.run_cross_harness([
            "--workspace", str(self.root / "workspace"), "--iteration", "1",
            "--manifest", str(manifest), "--routes", str(routes),
            "--seed", "1", "--approve", "23",
        ])

        self.assertEqual(status, 0)
        self.assertEqual(call_log.read_text().splitlines(), ["call"] * 23)

    def test_plan_reports_all_calls_without_invoking_a_route(self):
        manifest = self.root / "evals.json"
        self.write_json(manifest, {
            "schema_version": 2,
            "arms": {"baseline": {}, "with_agent": {}, "with_rule": {}},
            "comparisons": [
                {"id": "agent", "primary": "with_agent", "baseline": "baseline"},
                {"id": "rule", "primary": "with_rule", "baseline": "baseline"},
            ],
            "evals": [{"id": 1, "name": "sample", "prompt": "Review.", "files": [], "assertions": ASSERTIONS}],
        })
        call_log = self.root / "calls.log"
        routes = self.root / "routes.json"
        self.write_json(routes, {"routes": {"fake": {
            "binary": "fake-harness", "model": "model",
            "argv": ["--prompt-file", "{prompt_file}"], "response": "text",
            "env": {"CALL_LOG": str(call_log)},
            "context_canary": "List visible artifact rules.",
            "forbidden_context_markers": ["SECRET_ARTIFACT"],
        }}})
        output = io.StringIO()

        with redirect_stdout(output):
            status = self.run_cross_harness([
                "--workspace", str(self.root / "workspace"), "--iteration", "1",
                "--manifest", str(manifest), "--routes", str(routes),
                "--comparison", "agent", "--repeats", "3", "--seed", "1", "--plan",
            ])

        self.assertEqual(status, 0)
        self.assertIn("6 benchmark runs and 2 route checks (8 provider calls)", output.getvalue())
        self.assertFalse(call_log.exists())
        self.assertFalse((self.root / "workspace").exists())

    def test_plan_rejects_invalid_route_before_a_provider_call(self):
        manifest = self.root / "invalid-route-evals.json"
        self.write_json(manifest, {
            "schema_version": 2, "arms": {"baseline": {}}, "comparisons": [],
            "evals": [{"id": 1, "name": "sample", "prompt": "Review.", "files": [], "assertions": ASSERTIONS}],
        })
        call_log = self.root / "invalid-route-calls.log"
        routes = self.root / "invalid-routes.json"
        self.write_json(routes, {"routes": {"fake": {
            "binary": "fake-harness", "model": "model",
            "argv": ["--prompt-file", "{unknown}"], "response": "text",
            "env": {"CALL_LOG": str(call_log)},
            "context_canary": "List visible artifact rules.",
            "forbidden_context_markers": ["SECRET_ARTIFACT"],
        }}})

        status = self.run_cross_harness([
            "--workspace", str(self.root / "invalid-route-workspace"), "--iteration", "1",
            "--manifest", str(manifest), "--routes", str(routes), "--seed", "1", "--plan",
        ])

        self.assertEqual(status, 1)
        self.assertFalse(call_log.exists())

    def test_invalid_assertions_fail_before_a_provider_call(self):
        manifest = self.root / "invalid-assertion-evals.json"
        self.write_json(manifest, {
            "schema_version": 2, "arms": {"baseline": {}}, "comparisons": [],
            "evals": [{
                "id": 1, "name": "sample", "prompt": "Review.", "files": [],
                "assertions": [{
                    "kind": "required_patterns",
                    "text": "The response keeps the required fact.",
                    "patterns": [],
                }],
            }],
        })
        call_log = self.root / "invalid-assertion-calls.log"
        routes = self.root / "invalid-assertion-routes.json"
        self.write_json(routes, {"routes": {"fake": {
            "binary": "fake-harness", "model": "model",
            "argv": ["--prompt-file", "{prompt_file}"], "response": "text",
            "env": {"CALL_LOG": str(call_log)},
            "context_canary": "List visible artifact rules.",
            "forbidden_context_markers": ["SECRET_ARTIFACT"],
        }}})

        status = self.run_cross_harness([
            "--workspace", str(self.root / "invalid-assertion-workspace"),
            "--iteration", "1", "--manifest", str(manifest),
            "--routes", str(routes), "--seed", "1",
        ])

        self.assertEqual(status, 1)
        self.assertFalse(call_log.exists())


if __name__ == "__main__":
    unittest.main()
