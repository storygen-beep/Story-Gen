# Jack's World - Story Structure

> Generated from TOML schema v0.2

## Story Progression

```mermaid
flowchart TD
    house_rules["House Rules<br/>📍 Home"]
    accidental_glimpse["The Accidental Glimpse<br/>📍 Bathroom"]
    house_rules --> |"chores_explained + love>=8"| accidental_glimpse
    angelas_struggle["The Bills<br/>📍 Kitchen"]
    accidental_glimpse --> |"jack_arrived_complete + trust>=4 + love>=5"| angelas_struggle
    jack_gets_hired["Apply Job<br/>📍 Cafe"]
    angelas_struggle --> |"bills_discovered + trust>=6"| jack_gets_hired
    angelas_evening["Her Routine<br/>📍 Living Room"]
    jack_gets_hired --> |"job_started + trust>=8"| angelas_evening
    first_rent_day["First Rent<br/>📍 Kitchen"]
    angelas_evening --> |"job_started + trust>=10 + money>=200"| first_rent_day
    late_night_kitchen["Can't Sleep<br/>📍 Kitchen"]
    first_rent_day --> |"first_rent_paid + trust>=14"| late_night_kitchen
    massage_offer["The Offer<br/>📍 Living Room<br/>🔓 kiss_unlocked"]
    late_night_kitchen --> |"towel_encounter_complete + first_kiss_complete + 2d since first_kiss_complete + love>=40 + trust>=18"| massage_offer
    towel_encounter["Towel Encounter<br/>📍 Bathroom"]
    massage_offer --> |"jack_arrived_complete + first_rent_paid + love>=20 + trust>=18"| towel_encounter
    first_kiss["The First Kiss<br/>📍 Living Room"]
    towel_encounter --> |"towel_encounter_complete + love>=25"| first_kiss
    activity_deep_conversation_angela["Deep Conversation<br/>📍 Living Room"]
    first_kiss --> |"kiss_unlocked + 1d since massage_offered + love>=20 + trust>=20"| activity_deep_conversation_angela
    event_bath_invitation["She Noticed<br/>📍 Bathroom<br/>🔓 oral_unlocked"]
    activity_deep_conversation_angela --> |"peek_unlocked + groping_unlocked + love>=60"| event_bath_invitation
    event_date_proposal["Somewhere Else<br/>📍 Kitchen"]
    event_bath_invitation --> |"oral_unlocked + love>=75 + trust>=25"| event_date_proposal
```

## Activities: Angela's Bedroom

```mermaid
flowchart LR
    subgraph Angela's_Morning["Angela's Morning"]
        direction TB
        Angela's_Morning_T1["T1<br/>peek_unlocked"]
    end
    subgraph Exploring_Kink["Exploring Kink"]
        direction TB
        Exploring_Kink_T8["T8<br/>love>=90 + trust>=30 + sex_unlocked + date_night_complete"]
    end
    subgraph Night_Together["Night Together"]
        direction TB
        Night_Together_T1["T1<br/>oral_unlocked + love>=60 + trust>=25"]
    end
    subgraph Spa/Massage["Spa/Massage"]
        direction TB
        Spa/Massage_T7["T7<br/>love>=40 + trust>=18 + massage_offered"]
    end
```

## Activities: Bathroom

```mermaid
flowchart LR
    subgraph Angela's_Bath["Angela's Bath"]
        direction TB
        Angela's_Bath_T1["T1<br/>peek_unlocked"]
    end
    subgraph Do_Laundry["Do Laundry"]
        direction TB
        Do_Laundry_T1["T1<br/>chores_explained"]
    end
```

## Activities: Cafe

```mermaid
flowchart LR
    subgraph Cafe_Shift["Cafe Shift"]
        direction TB
        Cafe_Shift_T1["T1<br/>job_started"]
        Cafe_Shift_T1["T1<br/>job_started"]
    end
    Cafe_Shift_T1 -.-> Cafe_Shift_T1
```

## Activities: Hotel Room

```mermaid
flowchart LR
    subgraph Date_Night_Hotel["Date Night Hotel"]
        direction TB
        Date_Night_Hotel_T1["T1<br/>date_proposed + love>=80 + trust>=30 + money>=300"]
    end
```

## Activities: Jack's Bedroom

```mermaid
flowchart LR
    subgraph Bed["Bed"]
        direction TB
        Bed_T1["T1 (fallback)"]
    end
```

## Activities: Kitchen

```mermaid
flowchart LR
    subgraph Breakfast_Together["Breakfast Together"]
        direction TB
        Breakfast_Together_T1["T1 (fallback)"]
    end
    subgraph Cook_Dinner["Cook Dinner"]
        direction TB
        Cook_Dinner_T1["T1<br/>chores_explained"]
    end
    subgraph Rent_Day["Rent Day"]
        direction TB
        Rent_Day_T2["T2<br/>first_rent_paid + 7d since rent_last_paid + money>=200"]
    end
    subgraph Wash_Dishes["Wash Dishes"]
        direction TB
        Wash_Dishes_T1["T1<br/>chores_explained"]
    end
```

## Activities: Living Room

```mermaid
flowchart LR
    subgraph Clean_Apartment["Clean Apartment"]
        direction TB
        Clean_Apartment_T1["T1<br/>chores_explained"]
    end
    subgraph Movie_Night["Movie Night"]
        direction TB
        Movie_Night_T1["T1 (fallback)"]
    end
```

## Activities: Street

```mermaid
flowchart LR
    subgraph Grocery_Shopping["Grocery Shopping"]
        direction TB
        Grocery_Shopping_T1["T1<br/>chores_explained"]
    end
```

## Gate Unlocks

| Story Canvas | Gate Flag | Unlocks |
|--------------|-----------|---------|
| The Offer | `kiss_unlocked` | T3 teasing |
| She Noticed | `oral_unlocked` | T6 oral |