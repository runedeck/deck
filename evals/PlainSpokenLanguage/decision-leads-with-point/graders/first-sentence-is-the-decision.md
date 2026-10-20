---
type: regex
pattern: '^(?:[#*_\s]*(?:Hi|Hello|Hey|Subject|Re)\b[^\n]*\n+)*(?=[^.!?\n]*JSON)(?=[^.!?\n]*\b(decided|decision|chose|choose|picked|going with|go with|settled on|will (store|use|keep|write|save)|switch(ing)? to)\b)'
flags: i
match: contains
weight: 1
---
