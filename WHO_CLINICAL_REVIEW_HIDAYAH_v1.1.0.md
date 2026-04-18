# WHO IMCI Technical Review
## HIDAYAH v1.1.0 - Clinical Danger Detection Engine

**Review Date:** December 2024
**Reviewer:** Technical Assessment (IMCI Alignment)
**Document Type:** Clinical Logic Compliance Review

---

## EXECUTIVE SUMMARY

HIDAYAH v1.1.0 demonstrates **substantial alignment** with WHO IMCI (Integrated Management of Childhood Illness) guidelines. The application implements a probabilistic risk assessment engine with uncertainty quantification—a methodologically sound approach for decision support in resource-limited settings.

**Overall Assessment: SATISFACTORY with recommendations**

| Domain | Score | Notes |
|--------|-------|-------|
| General Danger Signs | ✅ Excellent | All 4 core signs included with correct urgency |
| Pneumonia Classification | ✅ Good | Fast breathing thresholds age-appropriate |
| Dehydration Assessment | ✅ Good | Plan A/B/C logic correctly mapped |
| Fever Classification | ✅ Good | Meningitis signs included |
| Young Infant (<2 months) | ✅ Good | PSBI criteria addressed |
| Severe Malnutrition | ✅ Good | SAM/MAM detection present |
| Measles Complications | ✅ Good | Eye and mouth complications covered |
| Ear Assessment | ✅ Adequate | Mastoiditis detection present |
| HIV Considerations | ⚠️ Partial | Present but UI incomplete |
| Anaemia Assessment | ⚠️ Partial | Pallor only; no haemoglobin |

---

## DETAILED ANALYSIS

### 1. GENERAL DANGER SIGNS (IMCI Core)

**IMCI Requirement:** Any ONE general danger sign = URGENT REFERRAL

| Sign | IMCI Definition | HIDAYAH Implementation | Status |
|------|-----------------|------------------------|--------|
| Not able to drink/breastfeed | Cannot swallow | ✅ `not_able_to_drink` (weight: 3.8) | Correct |
| Vomits everything | Cannot retain fluids | ✅ `vomits_everything` (weight: 3.5) | Correct |
| Convulsions | Seizure during illness | ✅ `convulsions` (weight: 4.2) | Correct |
| Lethargic/unconscious | Abnormally sleepy | ✅ `lethargic_unconscious` (weight: 4.8) | Correct |

**Assessment:** All general danger signs are correctly implemented with appropriately high weights ensuring RED classification when present. The weight for "lethargic/unconscious" is highest (4.8), which aligns with IMCI priority.

**Recommendation:** None required.

---

### 2. COUGH/DIFFICULTY BREATHING (Pneumonia Classification)

**IMCI Fast Breathing Thresholds:**
- 0-2 months: ≥60 breaths/min
- 2-12 months: ≥50 breaths/min
- 12 months-5 years: ≥40 breaths/min

**HIDAYAH Implementation:**
```javascript
age_priors: {
    "neonate_early":  { fast_breathing_threshold: 60 },
    "neonate":        { fast_breathing_threshold: 60 },
    "young_infant":   { fast_breathing_threshold: 60 },
    "infant":         { fast_breathing_threshold: 50 },
    "young_child":    { fast_breathing_threshold: 40 }
}
```

**Assessment:** Thresholds are IMCI-compliant.

| Sign | IMCI Classification | HIDAYAH | Status |
|------|---------------------|---------|--------|
| Fast breathing alone | PNEUMONIA | ✅ weight: 1.8 | Correct |
| Chest indrawing | SEVERE PNEUMONIA | ✅ weight: 2.8, urgent | Correct |
| Stridor when calm | SEVERE PNEUMONIA | ✅ weight: 3.2, urgent | Correct |
| Nasal flaring | Respiratory distress | ✅ weight: 2.0 | Correct |
| Grunting | SEVERE PNEUMONIA | ✅ weight: 2.5, urgent | Correct |
| Cyanosis | SEVERE PNEUMONIA | ✅ weight: 3.8, urgent | Correct |

**Recommendation:** Consider adding "wheeze" as a sign for classification of asthma/wheezing illness per updated IMCI chart booklet.

---

### 3. DIARRHOEA & DEHYDRATION

**IMCI Dehydration Classification:**

| Plan | Signs Required | HIDAYAH Implementation |
|------|----------------|------------------------|
| Plan C (Severe) | 2+ of: lethargic, sunken eyes, unable to drink, skin pinch very slow | ✅ `severe_dehydration_compound` interaction |
| Plan B (Some) | 2+ of: restless, sunken eyes, drinks eagerly, skin pinch slow | ✅ `dehydration_compound` interaction |
| Plan A (None) | No dehydration signs | ✅ Default state |

**Assessment:** Dehydration logic correctly implements IMCI two-sign requirement for classification.

**Strengths:**
- Sunken fontanelle included (important for infants)
- Blood in stool correctly triggers DYSENTERY classification
- Persistent diarrhoea (≥14 days) tracked separately

**Recommendation:** Add "dry mouth/tongue" sign for more complete assessment.

---

### 4. FEVER ASSESSMENT

**IMCI Fever Classifications:**

| Condition | Signs | HIDAYAH | Status |
|-----------|-------|---------|--------|
| Very Severe Febrile Disease | Fever + general danger sign | ✅ `fever_plus_convulsions` interaction | Correct |
| Meningitis | Fever + stiff neck | ✅ `fever_plus_stiff_neck` interaction | Correct |
| Meningitis (infants) | Fever + bulging fontanelle | ✅ `fever_plus_bulging_fontanelle` | Correct |
| Malaria (endemic area) | Fever + no other cause | ✅ `malaria_endemic` modifier | Correct |
| Severe Malaria | Fever + severe pallor (endemic) | ✅ `malaria_severe_anaemia` interaction | Correct |

**Assessment:** Fever logic is comprehensive and correctly handles meningitis detection.

**Strength:** Hypothermia (<35.5°C) is correctly flagged as serious sign for young infants.

**Recommendation:** Consider adding "runny nose" to distinguish viral from bacterial infections.

---

### 5. YOUNG INFANT (<2 MONTHS) - PSBI Assessment

**IMCI Young Infant Signs of Possible Serious Bacterial Infection (PSBI):**

| Sign | HIDAYAH Implementation | Status |
|------|------------------------|--------|
| Not feeding well | ✅ `poor_feeding` (weight: 2.0) | Correct |
| Movement reduced | ✅ `movement_reduced` (weight: 2.0) | Correct |
| Movement only when stimulated | ✅ `movement_only_stimulated` (weight: 3.0, urgent) | Correct |
| No movement | ✅ `no_movement` (weight: 4.5, urgent) | Correct |
| Severe chest indrawing | ✅ Inherited from breathing assessment | Correct |
| Fever (≥37.5°C) or hypothermia (<35.5°C) | ✅ Both tracked | Correct |
| Umbilical redness | ✅ `umbilicus_red` (weight: 1.5) | Correct |
| Umbilical redness extending | ✅ `umbilicus_red_extending` (weight: 2.5, urgent) | Correct |
| Skin pustules | ✅ `skin_pustules` / `skin_pustules_many` | Correct |
| Jaundice (palms/soles) | ✅ `jaundice_severe` (weight: 3.0, urgent) | Correct |
| Jaundice in first 24h | ✅ `jaundice_early` (weight: 2.5, urgent) | Correct |

**Assessment:** PSBI criteria are comprehensively implemented.

**Strength:** Early neonate (0-7 days) is correctly separated from late neonate (7-28 days) with higher baseline risk.

**Recommendation:** Consider adding "fast breathing ≥60/min in young infant" as standalone urgent sign per updated PSBI guidelines.

---

### 6. MALNUTRITION ASSESSMENT

**IMCI Severe Acute Malnutrition (SAM) Signs:**

| Sign | HIDAYAH | Status |
|------|---------|--------|
| Visible severe wasting | ✅ `visible_severe_wasting` (urgent) | Correct |
| Oedema of both feet | ✅ `oedema_both_feet` (urgent) | Correct |
| MUAC <11.5cm (red) | ✅ `muac_red` | Correct |
| MUAC 11.5-12.4cm (yellow) | ✅ `muac_yellow` | Correct |

**Assessment:** SAM detection is correctly implemented.

**Strength:** Interaction `malnutrition_plus_infection` correctly escalates risk when malnourished child has infection—this aligns with IMCI guidance that SAM + any infection = URGENT REFERRAL.

**Recommendation:** Add weight-for-height Z-score option if feasible.

---

### 7. MEASLES COMPLICATIONS

**IMCI Measles Classification:**

| Classification | Signs | HIDAYAH | Status |
|----------------|-------|---------|--------|
| Severe Complicated Measles | Clouding of cornea | ✅ `cornea_clouding` (urgent) | Correct |
| Severe Complicated Measles | Deep mouth ulcers | ✅ `deep_mouth_ulcers` (urgent) | Correct |
| Complicated Measles | Pus in eye | ✅ `pus_in_eye` | Correct |
| Complicated Measles | Mouth ulcers | ✅ `mouth_ulcers` | Correct |
| Measles | Rash + history | ✅ `measles_rash` | Correct |

**Assessment:** Measles complications are well-covered.

---

### 8. EAR ASSESSMENT

| Classification | Signs | HIDAYAH | Status |
|----------------|-------|---------|--------|
| Mastoiditis | Tender swelling behind ear | ✅ `mastoid_tenderness` (urgent) | Correct |
| Acute Ear Infection | Ear pain, discharge <14d | ✅ `ear_pain`, `ear_discharge_acute` | Correct |
| Chronic Ear Infection | Discharge ≥14 days | ✅ `ear_discharge` | Correct |

**Assessment:** Ear assessment is adequate.

---

## METHODOLOGICAL STRENGTHS

### 1. Uncertainty Quantification
The Monte Carlo approach with 200 samples and 80% credible intervals is methodologically sound. This acknowledges diagnostic uncertainty—critical in low-resource settings where clinical signs may be ambiguous.

### 2. Bayesian Framework
Using log-odds (logit) transformation with Gaussian noise is appropriate for combining multiple risk factors. The sigmoid transformation back to probability space is correct.

### 3. Interaction Effects
The model correctly implements super-additive interactions (e.g., fever + stiff neck = meningitis) which reflects true clinical syndromes.

### 4. Exclusive Factor Groups
The `max_only` mode for mutually exclusive signs (e.g., fever levels) prevents double-counting—this is correct implementation.

### 5. Vulnerability Thresholds
Lower thresholds for vulnerable populations (neonates, malnourished) reflects IMCI principle of erring toward referral for high-risk groups.

---

## GAPS AND RECOMMENDATIONS

### HIGH PRIORITY

1. **HIV Assessment UI Incomplete**
   - The MODEL includes HIV weights but UI does not expose HIV status question
   - **Recommendation:** Add HIV status question to Step 6 or dedicated step
   - This is critical in high-prevalence settings

2. **Throat Assessment Missing**
   - IMCI includes "Sore Throat" assessment (streptococcal pharyngitis)
   - **Recommendation:** Add throat pain + exudate question

3. **Feeding Assessment for Young Infants**
   - IMCI asks about attachment/positioning problems
   - **Recommendation:** Add breastfeeding assessment for <2 months

### MEDIUM PRIORITY

4. **Wheezing/Asthma**
   - Not currently captured
   - **Recommendation:** Add "wheeze" to breathing assessment

5. **Vitamin A Status**
   - IMCI recommends Vitamin A for measles, severe malnutrition
   - **Recommendation:** Add reminder in guidance output

6. **Immunization History**
   - `no_immunization` weight exists but UI missing
   - **Recommendation:** Add immunization status question

### LOW PRIORITY

7. **Growth Monitoring**
   - Weight-for-age/height Z-scores would improve malnutrition detection
   - **Recommendation:** Consider optional growth chart input

8. **Haemoglobin Measurement**
   - Would improve anaemia classification beyond pallor
   - **Recommendation:** Add optional Hb input field

---

## WEIGHT CALIBRATION ASSESSMENT

| Sign | Current Weight | IMCI Alignment | Recommendation |
|------|----------------|----------------|----------------|
| `lethargic_unconscious` | 4.8 | ✅ Highest = correct | None |
| `convulsions` | 4.2 | ✅ Very high = correct | None |
| `stiff_neck` | 4.2 | ✅ Very high = correct | None |
| `no_movement` | 4.5 | ✅ Very high = correct | None |
| `cyanosis` | 3.8 | ✅ High = correct | None |
| `cornea_clouding` | 3.5 | ✅ High = correct | None |
| `fast_breathing` | 1.8 | ⚠️ May be too low | Consider 2.0-2.2 |
| `blood_in_stool` | 2.0 | ⚠️ May be too low | Consider 2.2-2.5 |

---

## DISCLAIMER REQUIREMENTS

The application correctly includes disclaimers stating:
- "This tool estimates danger — it does not diagnose"
- "Not a diagnostic tool"
- "Always seek professional care if concerned"

**Recommendation:** Add more prominent disclaimer that this is **NOT an official WHO tool** and has not been formally validated by WHO.

---

## CONCLUSION

HIDAYAH v1.1.0 demonstrates **strong technical alignment** with WHO IMCI guidelines. The probabilistic approach with uncertainty quantification is methodologically appropriate for clinical decision support.

**Key Strengths:**
- Comprehensive coverage of IMCI danger signs
- Correct age-specific thresholds
- Appropriate interaction effects
- Young infant PSBI criteria well-implemented
- Uncertainty quantification appropriate for field use

**Areas for Improvement:**
- Complete HIV assessment UI
- Add throat/sore throat assessment
- Add immunization status input
- More prominent "not official WHO" disclaimer

**Recommendation for Use:**
- Suitable for **training and educational purposes**
- Could be considered for **pilot field testing** with appropriate clinical oversight
- Should **not replace** clinical judgment or formal IMCI training
- Requires **validation study** before wider deployment

---

## APPENDIX: IMCI CLASSIFICATION MAPPING

| IMCI Classification | HIDAYAH Code | Urgency |
|---------------------|--------------|---------|
| Very Severe Disease/PSBI | `GENERAL_DANGER_SIGN`, `SERIOUS_BACTERIAL_INFECTION` | RED |
| Severe Pneumonia | `SEVERE_PNEUMONIA` | RED |
| Severe Dehydration | `SEVERE_DEHYDRATION` | RED |
| Meningitis | `MENINGITIS` | RED |
| Severe Malaria | `SEVERE_MALARIA` | RED |
| Mastoiditis | `MASTOIDITIS` | RED |
| Severe Complicated Measles | `SEVERE_COMPLICATED_MEASLES` | RED |
| Severe Malnutrition | `SEVERE_MALNUTRITION`, `SEVERE_ACUTE_MALNUTRITION` | RED |
| Severe Anaemia | `SEVERE_ANAEMIA` | RED |
| Pneumonia | `PNEUMONIA` | AMBER |
| Some Dehydration | `SOME_DEHYDRATION` | AMBER |
| Dysentery | `DYSENTERY` | AMBER |
| Acute Ear Infection | `ACUTE_EAR_INFECTION` | AMBER |
| Complicated Measles | `COMPLICATED_MEASLES` | AMBER |
| Fever (uncomplicated) | `FEVER` | GREEN |
| Cough (no pneumonia) | `COUGH_NO_PNEUMONIA` | GREEN |
| No Dehydration | `NO_DEHYDRATION` | GREEN |

---

*This review is for technical assessment purposes. HIDAYAH is not an official WHO product and has not been formally endorsed or validated by the World Health Organization.*
