#!/bin/bash

# Path to the pagefind-ui.js file
FILE="_site/pagefind/pagefind-ui.js"

# Original expression to find
ORIGINAL_EXPRESSION='placeholder:"Search",clear_search:"Clear"'

# Replacement expression
NEW_EXPRESSION='placeholder:"can\'t steer unless already moving",clear_search:"infoBAG"'

# Use sed to perform the replacement
sed -i "s/$ORIGINAL_EXPRESSION/$NEW_EXPRESSION/g" "$FILE"

echo "Replacement complete."
