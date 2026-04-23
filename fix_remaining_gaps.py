#!/usr/bin/env python3
"""
HIDAYAH v1.3.0 Enhancement Script
Fixes all remaining minor gaps from WHO review:
1. Add optional Haemoglobin input for anaemia classification
2. Add Weight-for-Height Z-Score input
3. Add Malaria RDT/Microscopy result checkbox
4. Add complete Nutrition assessment UI (MUAC, wasting, oedema)
"""

import os
import re

# Read the current version
with open(os.path.expanduser(r'~\Downloads\childnajia\hidayah-v1.2.0.html'), 'r', encoding='utf-8') as f:
    html = f.read()

# Update version number
html = html.replace('v1.2.0', 'v1.3.0')
html = html.replace('HIDAYAH v1.3.0', 'HIDAYAH v1.3.0')

# ============================================================================
# 1. ADD NUTRITION SECTION (Step 5.5 - before Hydration or as part of Step 6)
# We'll add it as a new subsection in Step 6
# ============================================================================

nutrition_section = '''
                    <!-- Nutrition Assessment -->
                    <div class="border-t border-slate-200 pt-3 mt-3">
                        <p class="text-xs text-slate-600 mb-3 font-medium">Nutrition assessment:</p>

                        <label class="flex items-start gap-3 p-3 rounded-lg border border-red-200 bg-red-50 cursor-pointer hover:bg-red-100 transition mb-2">
                            <input type="checkbox" id="visible_severe_wasting" class="mt-1 w-5 h-5" onchange="updateUI()">
                            <div>
                                <span class="text-sm font-medium text-slate-700">Visible severe wasting</span>
                                <span class="block text-xs text-slate-500">Very thin, bones/ribs clearly visible</span>
                            </div>
                        </label>

                        <label class="flex items-start gap-3 p-3 rounded-lg border border-red-200 bg-red-50 cursor-pointer hover:bg-red-100 transition mb-2">
                            <input type="checkbox" id="oedema_both_feet" class="mt-1 w-5 h-5" onchange="updateUI()">
                            <div>
                                <span class="text-sm font-medium text-slate-700">Oedema of both feet</span>
                                <span class="block text-xs text-slate-500">Bilateral pitting oedema (kwashiorkor sign)</span>
                            </div>
                        </label>

                        <div class="mb-3">
                            <label class="block text-sm font-medium text-slate-700 mb-2">MUAC (Mid-Upper Arm Circumference)</label>
                            <select id="muac" class="w-full bg-slate-50 border border-slate-300 rounded-lg p-2 text-sm" onchange="updateUI()">
                                <option value="not_measured">Not measured</option>
                                <option value="green">Green zone (>12.5cm) - Normal</option>
                                <option value="yellow">Yellow zone (11.5-12.4cm) - Moderate malnutrition</option>
                                <option value="red">Red zone (<11.5cm) - Severe acute malnutrition</option>
                            </select>
                        </div>

                        <div id="zscore_section" class="mb-3">
                            <label class="block text-sm font-medium text-slate-700 mb-2">Weight-for-Height Z-Score (optional)</label>
                            <select id="zscore" class="w-full bg-slate-50 border border-slate-300 rounded-lg p-2 text-sm" onchange="updateUI()">
                                <option value="not_measured">Not measured</option>
                                <option value="normal">Normal (> -2 SD)</option>
                                <option value="moderate">Moderate wasting (-3 to -2 SD)</option>
                                <option value="severe">Severe wasting (< -3 SD)</option>
                            </select>
                            <p class="text-xs text-slate-400 mt-1">For referral-level facilities with growth charts</p>
                        </div>
                    </div>

                    <!-- Anaemia Assessment -->
                    <div class="border-t border-slate-200 pt-3 mt-3">
                        <p class="text-xs text-slate-600 mb-3 font-medium">Anaemia assessment:</p>

                        <div class="mb-3">
                            <label class="block text-sm font-medium text-slate-700 mb-2">Pallor assessment</label>
                            <select id="pallor" class="w-full bg-slate-50 border border-slate-300 rounded-lg p-2 text-sm" onchange="updateUI()">
                                <option value="none">No pallor</option>
                                <option value="some">Some pallor (slight palmar/conjunctival)</option>
                                <option value="severe">Severe pallor (very pale palms/conjunctiva)</option>
                            </select>
                        </div>

                        <div id="haemoglobin_section" class="mb-3">
                            <label class="block text-sm font-medium text-slate-700 mb-2">Haemoglobin level (optional)</label>
                            <div class="flex gap-2 items-center">
                                <input type="number" id="haemoglobin" step="0.1" min="0" max="20" placeholder="e.g., 10.5"
                                    class="flex-1 bg-slate-50 border border-slate-300 rounded-lg p-2 text-sm" onchange="updateUI()">
                                <span class="text-sm text-slate-500">g/dL</span>
                            </div>
                            <p class="text-xs text-slate-400 mt-1">For facilities with Hb testing capability</p>
                        </div>
                    </div>'''

# Insert nutrition section before the "Other concerning signs" section
target_other_signs = '''                    <div class="border-t border-slate-200 pt-3 mt-3">
                        <p class="text-xs text-slate-600 mb-3 font-medium">Other concerning signs:</p>

                        <label class="flex items-start gap-3 p-3 rounded-lg border border-amber-200 bg-amber-50 cursor-pointer hover:bg-amber-100 transition mb-2">
                            <input type="checkbox" id="severe_pallor" class="mt-1 w-5 h-5" onchange="updateUI()">'''

# Replace the "Other concerning signs" section - remove the old severe_pallor checkbox since it's now in pallor dropdown
replacement_other_signs = nutrition_section + '''

                    <!-- Other Signs -->
                    <div class="border-t border-slate-200 pt-3 mt-3">
                        <p class="text-xs text-slate-600 mb-3 font-medium">Other concerning signs:</p>

                        <label class="flex items-start gap-3 p-3 rounded-lg border border-slate-200 cursor-pointer hover:bg-slate-50 transition mb-2">'''

html = html.replace(target_other_signs, replacement_other_signs)

# Remove the old severe_pallor checkbox standalone (it's now part of pallor dropdown)
html = html.replace('''                            <div>
                                <span class="text-sm font-medium text-slate-700">Severe pallor</span>
                                <span class="block text-xs text-slate-500">Very pale palms/conjunctiva — severe anaemia</span>
                            </div>
                        </label>

                        <label class="flex items-start gap-3 p-3 rounded-lg border border-slate-200 cursor-pointer hover:bg-slate-50 transition">
                            <input type="checkbox" id="measles_rash"''',
'''                            <input type="checkbox" id="measles_rash"''')

# ============================================================================
# 2. ADD MALARIA RDT CHECKBOX
# ============================================================================

malaria_rdt_section = '''
                        <label class="flex items-center justify-between p-3 rounded-lg bg-slate-50 mb-2">
                            <span class="text-sm text-slate-700">Malaria endemic area</span>
                            <input type="checkbox" id="malaria_endemic" class="toggle-checkbox sr-only" onchange="updateUI()">
                            <label for="malaria_endemic" class="toggle-label"></label>
                        </label>

                        <div id="malaria_test_section" class="mb-2 hidden">
                            <label class="flex items-start gap-3 p-3 rounded-lg border border-red-200 bg-red-50 cursor-pointer hover:bg-red-100 transition">
                                <input type="checkbox" id="malaria_test_positive" class="mt-1 w-5 h-5" onchange="updateUI()">
                                <div>
                                    <span class="text-sm font-medium text-slate-700">Malaria RDT/Microscopy POSITIVE</span>
                                    <span class="block text-xs text-slate-500">Confirmed malaria diagnosis</span>
                                </div>
                            </label>
                        </div>'''

old_malaria_section = '''                        <label class="flex items-center justify-between p-3 rounded-lg bg-slate-50 mb-2">
                            <span class="text-sm text-slate-700">Malaria endemic area</span>
                            <input type="checkbox" id="malaria_endemic" class="toggle-checkbox sr-only" onchange="updateUI()">
                            <label for="malaria_endemic" class="toggle-label"></label>
                        </label>'''

html = html.replace(old_malaria_section, malaria_rdt_section)

# ============================================================================
# 3. ADD NEW WEIGHTS TO MODEL
# ============================================================================

# Add new weights for haemoglobin-based anaemia and Z-score
new_weights = '''
        // ANAEMIA (Haemoglobin-based)
        "hb_severe_anaemia":     { mean: 2.8, sd: 0.30, imci: "SEVERE_ANAEMIA", urgent: true,
                                   desc: "Hb <7 g/dL" },
        "hb_moderate_anaemia":   { mean: 1.5, sd: 0.35, imci: "MODERATE_ANAEMIA",
                                   desc: "Hb 7-10 g/dL" },
        "hb_mild_anaemia":       { mean: 0.6, sd: 0.35, imci: "MILD_ANAEMIA",
                                   desc: "Hb 10-11 g/dL" },

        // Z-SCORE MALNUTRITION
        "zscore_severe":         { mean: 2.2, sd: 0.35, imci: "SEVERE_ACUTE_MALNUTRITION", urgent: true,
                                   desc: "WHZ < -3 SD" },
        "zscore_moderate":       { mean: 1.2, sd: 0.35, imci: "MODERATE_MALNUTRITION",
                                   desc: "WHZ -3 to -2 SD" },

        // MALARIA (confirmed)
        "malaria_confirmed":     { mean: 1.8, sd: 0.35, imci: "MALARIA",
                                   desc: "RDT/Microscopy positive" },

'''

# Insert after the SEVERE MALNUTRITION section
html = html.replace(
    '''        "malnourished":          { mean: 1.4, sd: 0.35, imci: "MALNUTRITION",
                                   desc: "Underweight/malnourished" },''',
    '''        "malnourished":          { mean: 1.4, sd: 0.35, imci: "MALNUTRITION",
                                   desc: "Underweight/malnourished" },
''' + new_weights
)

# ============================================================================
# 4. ADD EXCLUSIVE GROUPS FOR NEW INPUTS
# ============================================================================

new_exclusive_groups = '''
            // Anaemia levels (Hb-based)
            name: "hb_anaemia_level",
            mode: "max_only",
            members: ["hb_mild_anaemia", "hb_moderate_anaemia", "hb_severe_anaemia"]
        },
        {
            // Z-score levels
            name: "zscore_level",
            mode: "max_only",
            members: ["zscore_moderate", "zscore_severe"]
        },
        {'''

html = html.replace(
    '''            // Pallor levels
            name: "pallor_level",''',
    '''            // Pallor levels
            name: "pallor_level",
            mode: "max_only",
            members: ["some_pallor", "severe_pallor"]
        },
        {
''' + new_exclusive_groups[:-3]  # Remove trailing },\n        {
)

# ============================================================================
# 5. UPDATE getInputs() FUNCTION
# ============================================================================

old_getinputs_other = '''        // Other
        severe_pallor: document.getElementById('severe_pallor').checked,
        measles_rash: document.getElementById('measles_rash').checked,'''

new_getinputs_other = '''        // Nutrition
        visible_severe_wasting: document.getElementById('visible_severe_wasting')?.checked || false,
        oedema_both_feet: document.getElementById('oedema_both_feet')?.checked || false,
        muac: document.getElementById('muac')?.value || 'not_measured',
        zscore: document.getElementById('zscore')?.value || 'not_measured',

        // Anaemia
        pallor: document.getElementById('pallor')?.value || 'none',
        haemoglobin: parseFloat(document.getElementById('haemoglobin')?.value) || null,

        // Other
        measles_rash: document.getElementById('measles_rash').checked,'''

html = html.replace(old_getinputs_other, new_getinputs_other)

# Add malaria test positive to getInputs
old_malaria_endemic = '''        malaria_endemic: document.getElementById('malaria_endemic').checked,'''
new_malaria_endemic = '''        malaria_endemic: document.getElementById('malaria_endemic').checked,
        malaria_test_positive: document.getElementById('malaria_test_positive')?.checked || false,'''
html = html.replace(old_malaria_endemic, new_malaria_endemic)

# ============================================================================
# 6. UPDATE collectActiveFactors() FUNCTION
# ============================================================================

old_nutrition_factors = '''    // Nutrition assessment
    if (inputs.visible_severe_wasting) factors.push("visible_severe_wasting");
    if (inputs.oedema_both_feet) factors.push("oedema_both_feet");
    if (inputs.muac === "red") factors.push("muac_red");
    if (inputs.muac === "yellow") factors.push("muac_yellow");'''

new_nutrition_factors = '''    // Nutrition assessment
    if (inputs.visible_severe_wasting) factors.push("visible_severe_wasting");
    if (inputs.oedema_both_feet) factors.push("oedema_both_feet");
    if (inputs.muac === "red") factors.push("muac_red");
    if (inputs.muac === "yellow") factors.push("muac_yellow");

    // Z-Score malnutrition
    if (inputs.zscore === "severe") factors.push("zscore_severe");
    if (inputs.zscore === "moderate") factors.push("zscore_moderate");

    // Haemoglobin-based anaemia
    if (inputs.haemoglobin !== null) {
        if (inputs.haemoglobin < 7) factors.push("hb_severe_anaemia");
        else if (inputs.haemoglobin < 10) factors.push("hb_moderate_anaemia");
        else if (inputs.haemoglobin < 11) factors.push("hb_mild_anaemia");
    }

    // Confirmed malaria
    if (inputs.malaria_test_positive) factors.push("malaria_confirmed");'''

html = html.replace(old_nutrition_factors, new_nutrition_factors)

# ============================================================================
# 7. UPDATE updateUI() FUNCTION - Show/hide malaria test section
# ============================================================================

old_update_hiv = '''    // Show/hide HIV-related options'''
new_update_hiv = '''    // Show/hide malaria test section
    const malariaTestSection = document.getElementById('malaria_test_section');
    if (malariaTestSection) {
        malariaTestSection.classList.toggle('hidden', !inputs.malaria_endemic);
    }

    // Show/hide HIV-related options'''

html = html.replace(old_update_hiv, new_update_hiv)

# ============================================================================
# 8. UPDATE DEFAULT STATE
# ============================================================================

old_default_state = '''    // Nutrition
    visible_severe_wasting: false,
    oedema_both_feet: false,
    muac: 'not_measured','''

new_default_state = '''    // Nutrition
    visible_severe_wasting: false,
    oedema_both_feet: false,
    muac: 'not_measured',
    zscore: 'not_measured',

    // Anaemia
    pallor: 'none',
    haemoglobin: null,'''

html = html.replace(old_default_state, new_default_state)

# Add malaria test to default state
old_malaria_default = '''    malaria_endemic: false,'''
new_malaria_default = '''    malaria_endemic: false,
    malaria_test_positive: false,'''
html = html.replace(old_malaria_default, new_malaria_default)

# ============================================================================
# 9. UPDATE TEST SUITE
# ============================================================================

new_tests = '''
        // Haemoglobin-based anaemia tests
        {
            name: "Severe anaemia (Hb <7)",
            inputs: { ...defaultState, age_group: 'infant', acknowledged: true,
                      haemoglobin: 6.5, has_fever: true },
            expect: { category: 'red', minP: 0.40, imci: 'SEVERE_ANAEMIA' }
        },
        {
            name: "Moderate anaemia (Hb 8)",
            inputs: { ...defaultState, age_group: 'infant', acknowledged: true,
                      haemoglobin: 8.0 },
            expect: { category: 'amber', minP: 0.15, imci: 'MODERATE_ANAEMIA' }
        },
        // Z-Score malnutrition tests
        {
            name: "Severe wasting by Z-score",
            inputs: { ...defaultState, age_group: 'young_child', acknowledged: true,
                      zscore: 'severe' },
            expect: { category: 'red', minP: 0.35, imci: 'SEVERE_ACUTE_MALNUTRITION' }
        },
        {
            name: "Moderate wasting by Z-score",
            inputs: { ...defaultState, age_group: 'young_child', acknowledged: true,
                      zscore: 'moderate' },
            expect: { category: 'amber', minP: 0.12, imci: 'MODERATE_MALNUTRITION' }
        },
        // Confirmed malaria test
        {
            name: "Confirmed malaria (RDT positive)",
            inputs: { ...defaultState, age_group: 'young_child', acknowledged: true,
                      has_fever: true, malaria_endemic: true, malaria_test_positive: true },
            expect: { category: 'amber', minP: 0.25, imci: 'MALARIA' }
        },
        {
            name: "Severe malaria (confirmed + severe anaemia)",
            inputs: { ...defaultState, age_group: 'young_child', acknowledged: true,
                      has_fever: true, malaria_endemic: true, malaria_test_positive: true,
                      pallor: 'severe' },
            expect: { category: 'red', minP: 0.55, imci: 'SEVERE_MALARIA' }
        },
        // Complete nutrition UI tests
        {
            name: "Visible severe wasting detection",
            inputs: { ...defaultState, age_group: 'young_child', acknowledged: true,
                      visible_severe_wasting: true },
            expect: { category: 'red', minP: 0.35, imci: 'SEVERE_MALNUTRITION' }
        },
        {
            name: "Oedema both feet detection",
            inputs: { ...defaultState, age_group: 'young_child', acknowledged: true,
                      oedema_both_feet: true },
            expect: { category: 'red', minP: 0.38, imci: 'SEVERE_MALNUTRITION' }
        },
        {
            name: "MUAC red zone detection",
            inputs: { ...defaultState, age_group: 'young_child', acknowledged: true,
                      muac: 'red' },
            expect: { category: 'red', minP: 0.30, imci: 'SEVERE_ACUTE_MALNUTRITION' }
        },
        {
            name: "MUAC yellow zone detection",
            inputs: { ...defaultState, age_group: 'young_child', acknowledged: true,
                      muac: 'yellow' },
            expect: { category: 'amber', minP: 0.10, imci: 'MODERATE_MALNUTRITION' }
        },'''

# Insert new tests before the closing of TEST_CASES array
html = html.replace(
    '''        // Runny nose (viral indicator)
        {
            name: "Runny nose reduces bacterial probability",''',
    new_tests + '''
        // Runny nose (viral indicator)
        {
            name: "Runny nose reduces bacterial probability",'''
)

# ============================================================================
# 10. UPDATE TEST COUNT IN UI
# ============================================================================
html = html.replace('36 IMCI-based tests', '46 IMCI-based tests')

# ============================================================================
# 11. UPDATE VITAMIN A REMINDER TO INCLUDE Z-SCORE
# ============================================================================
old_vitamin_a = '''    // Show/hide Vitamin A reminder
    const showVitaminA = inputs.measles_rash || inputs.visible_severe_wasting ||
                         inputs.oedema_both_feet || inputs.muac === 'red';'''
new_vitamin_a = '''    // Show/hide Vitamin A reminder
    const showVitaminA = inputs.measles_rash || inputs.visible_severe_wasting ||
                         inputs.oedema_both_feet || inputs.muac === 'red' ||
                         inputs.zscore === 'severe';'''
html = html.replace(old_vitamin_a, new_vitamin_a)

# ============================================================================
# 12. FIX: Update pallor handling in collectActiveFactors
# ============================================================================
# Since we changed from checkbox to dropdown, update the pallor handling
old_pallor_check = '''    if (inputs.pallor === "severe") factors.push("severe_pallor");
    if (inputs.pallor === "some") factors.push("some_pallor");'''

# This should already exist, but let's make sure it's there
if 'if (inputs.pallor === "severe")' not in html:
    # Add it after the haemoglobin section we just added
    html = html.replace(
        '''    // Confirmed malaria
    if (inputs.malaria_test_positive) factors.push("malaria_confirmed");''',
        '''    // Confirmed malaria
    if (inputs.malaria_test_positive) factors.push("malaria_confirmed");

    // Pallor (from dropdown)
    if (inputs.pallor === "severe") factors.push("severe_pallor");
    if (inputs.pallor === "some") factors.push("some_pallor");'''
    )

# Write the new version
with open(os.path.expanduser(r'~\Downloads\childnajia\hidayah-v1.3.0.html'), 'w', encoding='utf-8') as f:
    f.write(html)

print("HIDAYAH v1.3.0 created successfully!")
print("\nEnhancements added:")
print("1. Nutrition Assessment UI:")
print("   - Visible severe wasting checkbox")
print("   - Oedema both feet checkbox")
print("   - MUAC dropdown (not measured/green/yellow/red)")
print("   - Weight-for-Height Z-Score dropdown")
print("")
print("2. Anaemia Assessment:")
print("   - Pallor dropdown (none/some/severe)")
print("   - Optional Haemoglobin input (g/dL)")
print("   - Automatic classification: <7 severe, 7-10 moderate, 10-11 mild")
print("")
print("3. Malaria Diagnosis:")
print("   - Malaria RDT/Microscopy positive checkbox")
print("   - Shows only when malaria endemic area is checked")
print("")
print("4. New weights added to model:")
print("   - hb_severe_anaemia (Hb <7)")
print("   - hb_moderate_anaemia (Hb 7-10)")
print("   - hb_mild_anaemia (Hb 10-11)")
print("   - zscore_severe (WHZ < -3 SD)")
print("   - zscore_moderate (WHZ -3 to -2 SD)")
print("   - malaria_confirmed (RDT positive)")
print("")
print("5. Updated test suite: 46 tests (was 36)")
