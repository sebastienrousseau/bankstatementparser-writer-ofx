# SPDX-FileCopyrightText: 2026 Sebastien Rousseau <sebastian.rousseau@gmail.com>
# SPDX-License-Identifier: Apache-2.0 OR MIT

# The README demo: the package's version, then both examples on the
# fixture in examples/data/ (transactions to OFX, and a CSV to OFX
# round trip). Render with `make demo`.

Output .github/demo.gif

Set Shell "bash"
Set FontSize 15
Set Width 1200
Set Height 1000
Set Padding 20
Set Theme "Catppuccin Mocha"
Set TypingSpeed 35ms

Hide
Type "export PS1='$ ' && clear"
Enter
Sleep 1s
Show

Type "poetry run python -c 'import bankstatementparser_writer_ofx as w; print(w.__version__)'"
Enter
Wait /\$$/
Sleep 1s

Type "poetry run python examples/01_basic_usage.py"
Enter
Wait /\$$/
Sleep 2s

Type "poetry run python examples/02_advanced_workflow.py"
Enter
Wait /\$$/
Sleep 4s
