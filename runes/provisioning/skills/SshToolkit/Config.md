# SSH config

`~/.ssh/config` is chezmoi output. Its source lives in the dotfiles tree. The dotfiles apply step creates `~/.ssh` with mode 700 and writes the config with mode 600.

## Layout on this machine

The blocks, in file order:

- `Host *` comes first. It sets `Port 22`, the keepalive directives (`ServerAliveInterval`, `ServerAliveCountMax`, `TCPKeepAlive`), `AddKeysToAgent yes`, `UseKeychain yes` behind `IgnoreUnknown UseKeychain`, `ForwardAgent yes`, and X11 forwarding off.
- `Host github.com` sets `IdentityFile ~/.ssh/<key>` for the resident key and `IdentitiesOnly yes`.
- `Include hosts` and `Include vendor/*` follow, with no `Host` or `Match` line between the GitHub block and them. They pull the private host inventory from `~/.ssh/hosts` and `~/.ssh/vendor`. Both are links into the private dotfiles tree. OpenSSH ignores a broken link in silence while that tree is not checked out.
- `Host */*` and `Host *+*` come last. Each sets a `ProxyCommand` that hops through the hosts named in the target: `ssh a/b/c` connects through `a`, then `b`, to `c`.
- The private inventory holds every other host. A host block never enters the public source.

## Two traps in this order

ssh uses the first value it obtains for each directive (`man ssh_config`). The `Host *` block at the top of this file therefore fixes `Port`, `ForwardAgent`, and the keepalive values for every host, the included ones too. A host block in `~/.ssh/hosts` cannot change its `Port` or turn `ForwardAgent` off. To change one of these for one host, give it on the command line (`ssh -p <port> <host>`, `ssh -o ForwardAgent=no <host>`), or move the directive out of `Host *` in the chezmoi source. `IdentityFile` is the exception: its values add up across blocks.

An `Include` inside a `Host` or `Match` block is conditional (`man ssh_config`): ssh reads the file only when that block matches. In the source the two `Include` lines sit inside the `Host github.com` block, because no `Host` or `Match` line closes it before them. ssh then reads the private inventory only for a connection to GitHub, and every other host from `~/.ssh/hosts` resolves to the `Host *` defaults. `ssh -G <host>` shows it: no setting from the inventory appears. The fix is one `Match all` line before the two `Include` lines, in the chezmoi source of the dotfiles. It closes the GitHub block and matches every host.

## Rules

- Do not edit `~/.ssh/config` by hand. Edit the chezmoi source and apply.
- `IdentitiesOnly yes` stays on the GitHub block. Without it ssh offers every loaded key until GitHub refuses the connection.
- `ssh -G <host>` prints the resolved settings with no connection. Run it after every change to the source.
- A rotated host key: `ssh-keygen -R <host>` removes the stale entry, then reconnect.
