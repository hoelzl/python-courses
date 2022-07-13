Write-Output "Installing SplitPackage1"
pip install .\SplitPackage1\dist\splitpackage_part1-0.0.1-py3-none-any.whl --force-reinstall
Write-Output "Installing SplitPackage2"
pip install .\SplitPackage2\dist\splitpackage_part2-0.0.1-py3-none-any.whl --force-reinstall
Write-Output "Trying to uninstall UsePackage (may print a warning)"
pip uninstall usepackage -y
Write-Output "Installing UsePackage"
pip install .\UsePackage\dist\usepackage-0.0.1-py3-none-any.whl
