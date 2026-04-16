DESIGN PATTERNS FOR DIFFERENT STORY NEEDS:

**Intimate/Private Spaces:**
```
Pattern: 1-2 entry connections + 1 clear exit
Operations: nest → set_entry_from (1-2 destinations)
Player Psychology: Focused, private, safe
Story Use: Bedrooms, studies, confession booths
```

**Social Hub Spaces:**
```
Pattern: 3-4 entry connections + clear exit
Operations: nest → set_entry_from (3-4 destinations)
Player Psychology: Comfortable exploration choices
Story Use: Living rooms, taverns, town squares
```

**Adventure/Exploration Spaces:**
```
Pattern: 4-6 entry connections + safety exit
Operations: create → multiple set_entry_from to exploration paths
Player Psychology: Exciting discovery with security
Story Use: Forests, dungeons, mysterious areas
```

**Hierarchical Container Spaces:**
```
Pattern: is_container + default_entry_location + nested rooms
Operations: create container → set_default_entry → nest rooms → connect rooms
Player Psychology: Layered exploration, spatial depth
Story Use: Buildings, compounds, ships
```

OPERATIONS IMPACT REFERENCE:

| Operation | Twee Output | What Player Sees | Psychology Impact |
|-----------|-------------|------------------|-------------------|
| set_entry_from | `[[Go to X->Location_X]]` | Clickable navigation choice | 2-3 = comfortable, 5+ = overwhelming |
| default_entry | `Enter House->Location_Room` | Direct container→room flow | Immersive, realistic entry |
| nest (alone) | Spatial context only | Location exists "inside" parent | Grounding but needs connections |
| is_container + default_entry | `[[Enter X->Default]]` | "Go deeper" exploration option | Layered discovery & depth |
| No connections | Only "Back to Navigation" | Dead end, trapped feeling | Anxiety, immersion break |
