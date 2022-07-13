Write-Output "Trying to uninstall SplitPackage1 (may print a warning)"
pip uninstall splitpackage-part1 -y
Write-Output "Installing SplitPackage1"
pip install -e .\SplitPackage1
Write-Output "Trying to uninstall SplitPackage2 (may print a warning)"
pip uninstall splitpackage-part2 -y
Write-Output "Installing SplitPackage2"
pip install -e .\SplitPackage2
Write-Output "Trying to uninstall UsePackage (may print a warning)"
pip uninstall usepackage -y
Write-Output "Installing UsePackage"
pip install -e .\UsePackage
