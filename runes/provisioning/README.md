# provisioning

Skills and rules for setting up a machine. They hold the facts that models lack: newer interfaces, house conventions, and tested fixes. The module holds instruction text only. The scripts that change a machine live in the provisioning codebase, outside the deck, so reading the module cannot change a machine.

## Selection

The default deployment leaves this module out. The `all` cast excludes `provisioning/**`, so a consumer that takes the `all` cast receives no provisioning rune. A `.rune` with `include: ['**']` asks for every rune by pattern, so it receives this module too. A consumer receives the module when it names the module:

~~~sh
rune add provisioning
rune install
~~~

Run both commands from the consumer directory. The first command adds `provisioning` to the `include` list of the `.rune` manifest, which selects every rune of the module.

## Script paths

A rune that tells the model to run a script gives the path inside the provisioning codebase as inline code: `$PROVISION_ROOT/scripts/<kind>/<name>.sh`. It never writes the path as a markdown link. Before the first script step, the rune gives one shell step that resolves the root:

~~~sh
PROVISION_ROOT="${PROVISION_ROOT:-$HOME/Developer/runedeck/provision}"
~~~

`defaults.yaml` records the same location under the key `PROVISION_ROOT`. No loader exports the configuration of a module yet, so a `config.yaml` override beside it has no effect today. A consumer that keeps the codebase elsewhere exports `PROVISION_ROOT` in the shell before the resolve step, which keeps a value that is already set.

## Checks

`scripts/check-provisioning-module` reports every file under the module that has an execute permission or opens with an interpreter line. Such a file belongs in the provisioning codebase.

`scripts/check-provisioning-evidence` refuses a rune without a comparison record at `docs/changes/<change>/comparisons/<Name>.json`. The record shows the same cases run with the rune and without it on at least two models. At least one model answers at least one case correctly only with the rune. `scripts/record-comparison` writes the record from a BenchArtifact workspace.

A rune in this module contains no personal name, email address, host name, account name, or secret.

## License

[EUPL-1.2](LICENSE)
