# This terrain generation toolset was co-created with Gemini / Google AI.

# heightmap.txt
    Rule: U is for places you don't want to add terrain.
        Space separated. A number represents the respective height.

# expanse.py
    Rule: Finds any target number (like 1) and duplicates it
        outward into any touching U empty spaces.

# fill.py
    Rule: Identifies cells completely enclosed by numbers and
        fills them with a higher value, leaving the outer layer as
        a border ring.

# flatten.py
    Rule: Finds the outer edges of a specific high layer
        and strips them back down to a lower value so the inner
        volume footprint becomes smaller.

# reduce.py
    Rule: Shrinks a specific number footprint from the outside
        inward, turning its outer edges back into U (empty space).
        This is the perfect counterpart to expanse.py for eroding
        structures or opening up cave entrances.

# mesh_generator_final.py
    Rule: generates terrain like map from the heightmap.txt

# mesh_generator_blocky.py
    Rule: generates a more blocky or wall like feel.

# mesh_generator_blocky_adjusted.py
    Rule: generates a more blocky or wall but apparently accommodates
        for multi layer mountains with cave generations. Likely
        with the U gaps - unvalidated.
