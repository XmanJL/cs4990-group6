# Raw CSV Layout (high_imm_pop.csv)

**Dataset:** NP2017_D1  
**Title:** Projected Population by Single Year of Age, Sex, Race, and Hispanic Origin for the United States (2016–2060)  
**Source:** U.S. Census Bureau, Population Division  
**Release Date:** September 2018

---

## Data Structure

**Sort Order of Observations:**

- SEX
- ORIGIN
- RACE
- YEAR

---

## Data Fields

| Variable          | Description                                       |
| ----------------- | ------------------------------------------------- |
| SEX               | Sex                                               |
| ORIGIN            | Hispanic origin                                   |
| RACE              | Race                                              |
| YEAR              | Year of projection (July 1, 2016 to July 1, 2060) |
| TOTAL_POP         | Total population (all ages combined)              |
| POP_0 ... POP_100 | Population by single year of age (0–99, and 100+) |

---

## Code Keys

### ORIGIN (Hispanic Origin)

| Code | Description  |
| ---- | ------------ |
| 0    | Total        |
| 1    | Not Hispanic |
| 2    | Hispanic     |

---

### RACE

| Code | Description                   |
| ---- | ----------------------------- |
| 0    | All races (codes 1–6)         |
| 1    | White alone                   |
| 2    | Black alone                   |
| 3    | AIAN alone                    |
| 4    | Asian alone                   |
| 5    | NHPI alone                    |
| 6    | Two or More Races             |
| 7    | White alone or in combination |
| 8    | Black alone or in combination |
| 9    | AIAN alone or in combination  |
| 10   | Asian alone or in combination |
| 11   | NHPI alone or in combination  |

---

### SEX

| Code | Description |
| ---- | ----------- |
| 0    | Both sexes  |
| 1    | Male        |
| 2    | Female      |

---

## Notes

- Hispanic origin is **an ethnicity, not a race**. Hispanics may be of any race.
- “In combination” means reporting more than one race.
- Race groups (codes 7–11) sum to more than total population due to overlap.
- Projections may differ from official population estimates.
- Use population estimates for current population when available.

---

## Abbreviations

| Term  | Meaning                                    |
| ----- | ------------------------------------------ |
| Black | Black or African American                  |
| AIAN  | American Indian and Alaska Native          |
| NHPI  | Native Hawaiian and Other Pacific Islander |
