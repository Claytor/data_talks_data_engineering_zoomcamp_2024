Generic python transformer to standardize column names
- `@transformer` decorator takes the columns as a string
    - replaces any spaces with underscores `.str.replace(' ', '_')`
    - replaces ensures all characters are lower-case `.str.lower()`\
- We are skipping the assertion here for funsies.