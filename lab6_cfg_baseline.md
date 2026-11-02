# Baseline CFG — sanitize_value()

```mermaid
flowchart TD
    A([Start]) --> B[normalized_key = key.lower()]
    B --> C{normalized_key in SENSITIVE_KEYS?}

    C -- Yes --> D[return REDACTED]
    D --> R([End])

    C -- No --> E{normalized_key == email?}
    E -- Yes --> F[return mask_email(value)]
    F --> R

    E -- No --> G{normalized_key == phone?}
    G -- Yes --> H[return mask_phone(value)]
    H --> R

    G -- No --> I{isinstance(value, dict)?}
    I -- Yes --> J[return sanitize_mapping(value)]
    J --> R

    I -- No --> K{isinstance(value, list)?}
    K -- No --> Q[return value]
    Q --> R

    K -- Yes --> L{next item exists?}
    L -- No --> P[return list]
    P --> R

    L -- Yes --> M{isinstance(item, dict)?}
    M -- Yes --> N[append sanitize_mapping(item)]
    M -- No --> O[append item]

    N --> L
    O --> L
