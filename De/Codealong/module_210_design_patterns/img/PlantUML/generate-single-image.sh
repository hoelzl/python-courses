#!/bin/bash
echo "Generating PNG image for $1..."
java -jar ../../../Tools/plantuml.jar -Sdpi=600 -Smonochrome=true -SclassFontName="DejaVu Sans" -SclassAttributeFontName="DejaVu Sans" $1
echo "Done."


