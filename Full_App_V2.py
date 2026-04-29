import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import subprocess
import sys
import json
import os
from cryptography.fernet import Fernet

# --- SECURITY LAYER ---
MASTER_KEY = b'idZndzyfvZoZxBkLvgZDEikatow6zF4W7gN_W6fQH4M='
ENCRYPTED_DATA = b'gAAAAABpvzXXqLjkvu7-ZfXXJ2WiScEAYKPtmNQnYSAYVe60Z-rtWeoOOdnWjmrDfztcryfPxSw2C13plCcKtohieHBlPCRLlGrwJ0ayaEdRR8FIecClb_zAg2w3DGg3UpvR32nRCqLGPdcUXlYsQa1M-WwC2mRh7KwaT8IVUiSkAV5omEC6WhXxBjka_vQuEmjExiOZ8ooC95uPgPvOK56xkY5x-YbVhuEOGBAxiUMhf6wS2JRylzpTTxlbCs6yrUfa_rH4AJPoTAuab_ZMV1qcu858hi0gzyB1mtF24RhfFIvOXeYoyG-bAOvnx6fA7lx2UNR7khiwYDzioswVK-S0m3mwftdLwvYqNU888cWu6yA0b0ChQd2i0Esl2PLHBZNx8WjhgzTQNuxQl4hzvkPOWKUAAzncAhaYvXquAxI6MOr4AVqI7egMwW6a_OvtndEW3dNeIIPFS0JE3QCFmXzw-fuFu6YB2mF7rTRJ8OqhTZGb1rWBjzpMr84gMrPLdBeksb5IC3en0O7aNlChM5rUzBXRF-0bpugGjsWcBBjHWdFHPlTM8owyYhd4AZPuRw6BwNwUlRx_ONJ7Rrj8TOdGIMf3asqhwZTQT6RATHPrNquhTsQdrb95Th-HAB9U3IQBG2sHrWnvThO2EVJyHJqn4lOAcwp-xdZHzrgEy1OcD6iNfkNrbm5qr6-5BaiGU6OJ4ybZ7j4AUDpUm-exJWapEERL7ImnsdlOVzRNMaBig-cPRg_54phwQTx6VlOl24t5GgKuDCRf9kTFp6HpRSuobD1eY623AxGBG1HMU4zrPX6J8M6fVNfQCgPiI0W2i9m_2fe6bj1lJ2enRD7WzGInXlpeTsZMiVkngYJzmNUOtml1G0j2dGvwOlKq7c5mEDluWWbvH5_blrnUMceqRkWwC7LfHUdX0STk_qi0JTfMtzdTEZhIDoyM5YJaLbJWyIUnsZ6CuklSNjfGYbvhuOiSDzjjRIlOZoY2-kbfOJdrDbzqQrGO7I4HWA2ISyqdr4WmdUXz3BfcJT8702tF8rHBO4LH-7Y5Pah2GrkP53aHpPj3m6ig-Bl6ggcP3G9B6NXYXty2WRv3JwRIibWQa4sorI2DRWZ4_Xb9EzD_70SMXIjZykosc0jAADMULqik9cxjMPpVCHfxMlaoZ1hjFIFqN1wxt3-6CC_H5OX9TXkR8s1pi-Iex4nVmmEhy2mCsE9QvS_Zq_8Qy0mB42cPFQk_Zl-myGxNBMR8RfFFwMlrO_TrUj0WCZBPoZfJg45sCLmXTCL85j1PvdIckMjGoFEAcFNdDTMV0-iPOIGb7o0ZAA9LGkjRe_ZKqDlD5VcRlIUxqrfyqkur2Ue_SgAq7wdbAnCeH5ypuHaH0PEJitbpg8XaJKXd7tSNkl83ECyLQBiwFv1OiCqnqMiflxYQOh9BWec_5qJZIheCR2gP4KtK8P8iBBpgvpcUqQKkfJJsB9wB_4SO1UeFzNdnFtDUeS7mmOaslyFiH0pwtPCCNKtWsu9wpgMFo-gtL18H9AEY5s23wUje8EwXTRZVNVA11BPksN9SxCfHuJrWYUjs9va4G9hi9v23UeFCbGPHVE4COQilqAtSMBFvjHMHxaW99e-9Y-daRLIqiwfpa_fbya3JPO91PKr8tDwd8bfX3nQfxAUGpp9ONk_qMt_FheWG_5q5ezAEsB_LlOUqJzRdJc6oXi5IDM9L3K6CHErVYfx60QhgPOUJnmN58Y6Q1q8EY-pvIyzzPoJVXqMsJ_M0toMX7M2k4_9ik9qYLAsPN2qERNIv4KOhZYJsBWiWPDisebI3MPMagiaGmCn3mgr9CGv6d2mvKZu_IFw8M9NqhqRf4xOkN6h3cKlcKNjhYemcIN7zamjvu5Ulvahqj3OqA7TxBXvgaiIsi5cvxtZiPNNmQOCV0tw2SUFKtAY2UnKWPwiAcwHIVqtIfjStrf184XV-he81qCVFLVRJfCYqc_lh7KJ5xmLflomhAL6Fm7kQYTogLu66izIlOsw3MnqyrQrLK3UHGGT6u8Jz1zJcNXFYjdd0gi6FM8l8aUHnnmeZCJm7Sm2yshIoSnQouvrz7t1bD4mQwfX5isH8y2r3qnSlhiv7y-k6FGO_VoGVfVjI5mefKnhkbj6Ug9qRN5_YzUnP08MX_rdJDyDbNbii1o-x7t2-KAsLSPtVahqGXXycSLx5pZe-OmV6s8qnvI2UgPY-GAeBb1Rr17Hp7ohOBEy0i_E0pzFWPjdqznlSIk_Bm11J0JvcH2DtFp2ebgSmU2GLWjUkc28fifSOj629j38xgyggM0DH4r7ZeBx040ANtoQatutz11yNQsfA62pQVU8_1KHYywyo61LnOetk9Uw9wojN8OQSg1_W6aajuBBQKX3fJW7rTgwsz_zfFY6q5xop1-QRfvanFccJ6Gosv0nwhBMd0R6ZpjvSKTUwktFH0ZP7VqjREEfw2nK3k0k97ZNTEPt2mOAze2U9ur_0_Ie6LEqgUqYUO_8QA-hJR7pAUPfp_CAkGcXuoDV4dp8zpMVxeOK5YGp3eLj81Li12nOfvdKTfwRsas8R4Gp327U3XrFLlt5QJPWoRGPTSirED0VwzgH_q-Q0Hu8GTb02kJhtc08_pkIcU-rrNy0oEYXYXR1S0CR53z0DMzaZWp17DFYdQGMYRI0EBasJFQdO33CsG3rdTGfbuVXjjqAzOCxiCLAyhd0_v6DMJPYCBa2FXd5iznK7lV_NGPPnk9nJrN_7fdOboDvdIZoncEHNQ0EkwyekmQoq5Z9PFqsZmBKFyzA3zMWGswT_TCmQOu3KUO9c0a8XrS2-0hN-SM0FwBOgWKzWDWFdwKHOAROIZ-0EUIEyeQmDEA7JkXGuOu68VUG_qjiRklxxd7m4qGZJlezfcWDgEEL8QA1WNYMLo_S-UgzhUyWo9XoREpciqTNNm7I7xBuNZMVFUVNdmBEtXYo1gOg0jC3SX1KlYYGtY4Z64W4_p_jnDXxsRfiApHHHtny4ESjK49uayUd37L_yrCV45xajYIqRhnyfdzbh-jkZti4QMG1hssZFIxWXouyznsIC1hcURl7v7mxVCUZEiifvklj9n8X-of7PHFJpgpt6GoqrmTdmlstyiofoFqfcb403vfrnYQKYyWeYwZ78_8Xw3DS4kfeRLKmxh0UhL31FaFnMQNgxvxF85lbFtofTJ6_Fyk1YDmuxGcCQiS3tKyWD-GLPZ_Jd_fEz4VADEZcsXYz2xyHGPC_O-Q5kA5m3AYPtBX2uK_YjMmAg'

try:
    MASTER_KEY = st.secrets["security"]["master_key"].encode('utf-8')
    ENCRYPTED_DATA = st.secrets["security"]["encrypted_data"].encode('utf-8')
except KeyError:
    st.error("Secrets not configured correctly in Streamlit Cloud.")
    st.stop()

def get_decrypted_creds():
    """Decrypts the service account JSON from memory."""
    f = Fernet(MASTER_KEY)
    decrypted_json = f.decrypt(ENCRYPTED_DATA)
    return json.loads(decrypted_json)

# --- 0. HELPER FUNCTIONS ---

def get_dna_stat(champ_name, stat_name, df_dna):
    """Helper to pull stats for the gank calculator."""
    if champ_name == "-": return 5.0
    row = df_dna[df_dna['Name'] == champ_name]
    if not row.empty:
        mapping = {"CC": "Control(CC)", "Mobility": "Mobility"}
        actual_col = mapping.get(stat_name, stat_name)
        return float(row.iloc[0].get(actual_col, 5.0))
    return 5.0

# --- ARCHETYPE WEIGHTING PROFILES ---
# Order: Lane, Counter, Synergy, Scaling, Damage, Gank
WEIGHTING_PROFILES = {
    "Standard": {
        "lane": 0.45,
        "counter": 0.20,
        "synergy": 0.20,
        "scaling": 0.075,
        "damage": 0.075,
        "gank": 0.0  # Not applicable for standard laners
    },
    "Jungle_Ganker": {
        "lane": 0.35,
        "counter": 0.15,
        "synergy": 0.15,
        "scaling": 0.075,
        "damage": 0.075,
        "gank": 0.20
    },
    "Jungle_Farmer": {
        "lane": 0.40,
        "counter": 0.20,
        "synergy": 0.15,
        "scaling": 0.075,
        "damage": 0.075,
        "gank": 0.10
    }
}

# --- PATH LOGIC: Dynamic Folder Detection ---
# This finds the directory where Full_App_V2.py is currently sitting
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(SCRIPT_DIR, "champion_pools.json")

def load_all_pools():
    """Loads the entire JSON file or creates a blank one if it doesn't exist."""
    if os.path.exists(DATA_PATH):
        try:
            with open(DATA_PATH, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            # If the file is corrupted or unreadable, return a fresh structure
            return {"Top": [], "Jungle": [], "Mid": [], "Bot": [], "Support": []}
    return {"Top": [], "Jungle": [], "Mid": [], "Bot": [], "Support": []}

def save_pool_for_role(role, pool_list):
    """Saves only the pool for the currently selected role."""
    all_data = load_all_pools()
    all_data[role] = pool_list
    with open(DATA_PATH, "w") as f:
        json.dump(all_data, f, indent=4)

def calculate_synergy_delta(my_champ, ally_champ, df_synergy):
    """
    Look up the pre-calculated Delta 2 for a specific pair.
    New Logic: No math required. Just find the number in the sheet.
    """
    if my_champ == "-" or ally_champ == "-":
        return 0.0

    # Clean inputs
    my_c = str(my_champ).strip()
    ally_c = str(ally_champ).strip()

    # The scraper uses: My_Lane(0), My_Champ(1), Ally_Lane(2), Ally_Champ(3), Duo_Winrate(4)
    # We look for rows where our champ and the ally champ appear together
    mask = (
        (df_synergy.iloc[:, 1].astype(str).str.strip() == my_c) & 
        (df_synergy.iloc[:, 3].astype(str).str.strip() == ally_c)
    )
    duo_row = df_synergy[mask]

    if duo_row.empty:
        # Check reverse (in case the database stored it as Ally-Me instead of Me-Ally)
        mask_rev = (
            (df_synergy.iloc[:, 1].astype(str).str.strip() == ally_c) & 
            (df_synergy.iloc[:, 3].astype(str).str.strip() == my_c)
        )
        duo_row = df_synergy[mask_rev]

    if not duo_row.empty:
        try:
            # Column 4 is our scraped Delta val
            return float(duo_row.iloc[0, 4])
        except (ValueError, TypeError):
            return 0.0
            
    return 0.0

if 'profiles' not in st.session_state:
    st.session_state.profiles = {
        "Top": ["Dr. Mundo", "Kled", "Camille", "Gnar"],
        "Jungle": ["Jarvan IV", "Vi"],
        "Mid": ["Viktor", "Sylas"],
        "Bot": ["Ezreal", "Kai'Sa"],
        "Support": ["Thresh", "Lulu"]
    }
    


# --- 1. INITIAL SETUP (Must be the very first Streamlit command) ---
st.set_page_config(page_title="ZeroTrust Draft", 
    layout="wide", 
    initial_sidebar_state="expanded",
    page_icon="D:\League_of_legends_App_Data\ZeroTrustDraft.ico",
    )

st.markdown("""
    <style>
    /* 1. COMPLETELY REMOVE THE TOGGLE BUTTONS */
    /* This targets the 'X' and the '>' and makes them invisible and unclickable */
    [data-testid="stSidebarCollapseButton"], 
    [data-testid="collapsedControl"] {
        display: none !important;
        visibility: hidden !important;
        pointer-events: none !important;
    }

    /* 2. FORCE THE WIDTH & PREVENT DRAGGING */
    /* This sets the width to exactly 350px and prevents the user from resizing it */
    [data-testid="stSidebar"] {
        min-width: 350px !important;
        max-width: 350px !important;
        width: 350px !important;
    }

    /* 3. FIX THE OVERFLOW (Ensures the dropdown arrows stay visible) */
    /* This prevents the grey bar from eating your dropdown menus */
    [data-testid="stSidebar"] > div:first-child {
        width: 350px !important;
        overflow-x: hidden !important;
    }
    </style>
    """, 
    unsafe_allow_html=True)
# This CSS hides the header, menu, and footer for a clean OBS look
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            /* This tightens up the padding for a more compact view */
            .block-container {padding-top: 2rem; padding-bottom: 2rem;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# --- 2. DATA INGESTION ENGINE ---

@st.cache_data
def fetch_sheet_data(sheet_name):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    
    # Use the decrypted dictionary instead of a file
    creds_dict = get_decrypted_creds()
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    
    client = gspread.authorize(creds)
    spreadsheet = client.open("ZeroTrustDraftDatabase") 
    worksheet = spreadsheet.worksheet(sheet_name)
    data = worksheet.get_all_records()
    return pd.DataFrame(data)



# --- 1. Load Data into the App Session ---
try:
    # 1. Load Consolidated Meta (Replaces the 5 individual role sheets)
    df_meta = fetch_sheet_data("Active_Meta")
    
    # Update the col_name to the new header
    col_name = 'Champion'

    # Parsing out individual DataFrames using Pandas filtering
    df_top = df_meta[df_meta['Role'] == 'Top'].copy()
    df_jng = df_meta[df_meta['Role'] == 'Jungle'].copy()
    df_mid = df_meta[df_meta['Role'] == 'Mid'].copy()
    df_bot = df_meta[df_meta['Role'] == 'Bot'].copy()
    df_sup = df_meta[df_meta['Role'] == 'Support'].copy()
    
    # Maintain the map for logic that iterates through roles
    ROLE_DF_MAP = {
        "Top": df_top,
        "Jungle": df_jng,
        "Mid": df_mid,
        "Bot": df_bot,
        "Support": df_sup
    }
    
    # 2. Load Core Data (Updated names to match new Migration Map)
    df_matchups = fetch_sheet_data("Champ_Matchups")
    df_synergy  = fetch_sheet_data("Synergy_Matrix")
    df_dna      = fetch_sheet_data("Champion_DNA")
    df_globalmatchups = fetch_sheet_data("Global_Matchups")
    df_lane_logic = fetch_sheet_data("Ref_Lane_Logic")
    df_scaling_logic = fetch_sheet_data("Ref_Scaling_Logic")

    # 3. Define Archetypes
    ARCHETYPES = ["Enchanter", "Juggernaut", "Assassin", "Catcher", "Battlemage", 
                  "Specialist", "Vanguard", "Marksman", "Warden", "Skirmisher", 
                  "Diver", "Artillery", "Burst"]
    
    # 4. Create Dropdown Lists (Using the new 'Champion' column)
    # This logic stays the same but now reads from your filtered DFs
    TOP_CHAMPS = sorted(df_top[col_name].unique().tolist()) + [f"{a}_Avg" for a in ARCHETYPES]
    JUNGLE_CHAMPS = sorted(df_jng[col_name].unique().tolist()) + [f"{a}_Avg" for a in ARCHETYPES]
    MID_CHAMPS = sorted(df_mid[col_name].unique().tolist()) + [f"{a}_Avg" for a in ARCHETYPES]
    BOT_CHAMPS = sorted(df_bot[col_name].unique().tolist()) + [f"{a}_Avg" for a in ARCHETYPES]
    SUPPORT_CHAMPS = sorted(df_sup[col_name].unique().tolist()) + [f"{a}_Avg" for a in ARCHETYPES]

    # 5. Build Master Pool List (OPTIMIZED)
    # Since all champions are in one sheet now, we can just get unique values from df_meta
    ALL_CHAMPS = sorted(df_meta[col_name].unique().tolist())
    
    CHAMP_LISTS = {
        "Top": TOP_CHAMPS,
        "Jungle": JUNGLE_CHAMPS,
        "Mid": MID_CHAMPS,
        "Bot": BOT_CHAMPS,
        "Support": SUPPORT_CHAMPS
    }

except Exception as e:
    # This will print the exact error to the screen so you can debug live
    st.error(f"CRITICAL DATABASE ERROR: {e}")
    st.stop() # This halts the app so it doesn't try to run with missing variables

# --- 3. USER INPUT AND DATA MODULATION ---
# --- PHASE 1: USER PROFILE (Sidebar) ---
with st.sidebar:
    user_role = st.selectbox("Select Your Role", ["Top", "Jungle", "Mid", "Bot", "Support"])
    
    # This now looks in the script's folder automatically
    saved_data = load_all_pools()
    default_pool = saved_data.get(user_role, [])

    my_pool = st.multiselect(
        f"Define {user_role} Pool", 
        options=ALL_CHAMPS, 
        default=default_pool
    )

    if st.button(f"💾 Save {user_role} Profile"):
        save_pool_for_role(user_role, my_pool)
        st.toast(f"Profile Saved to {DATA_PATH}") # Using st.toast for a clean notification
    st.divider()
    
# --- PHASE 2: DRAFT INTAKE (Main Screen) ---
st.title("🎮 Live Draft Analyzer")

col1, col2 = st.columns(2)

with col1:
    st.subheader("🔵 Blue Side (Your Team)")
    
    # Logic: (my_pool if user_role == "Role" else FULL_LIST)
    # This keeps your role focused while keeping others flexible.
    
    blue_top = st.selectbox("Blue Top", 
        ["-"] + (my_pool if user_role == "Top" else TOP_CHAMPS), key="b_top")
        
    blue_jng = st.selectbox("Blue Jungle", 
        ["-"] + (my_pool if user_role == "Jungle" else JUNGLE_CHAMPS), key="b_jng")
        
    blue_mid = st.selectbox("Blue Mid", 
        ["-"] + (my_pool if user_role == "Mid" else MID_CHAMPS), key="b_mid")
        
    blue_bot = st.selectbox("Blue Bot", 
        ["-"] + (my_pool if user_role == "Bot" else BOT_CHAMPS), key="b_bot")
        
    blue_sup = st.selectbox("Blue Support", 
        ["-"] + (my_pool if user_role == "Support" else SUPPORT_CHAMPS), key="b_sup")
    st.write("") # Just a spacer
def reset_draft():
    for key in ["b_top", "b_jng", "b_mid", "b_bot", "b_sup", 
                "r_top", "r_jng", "r_mid", "r_bot", "r_sup"]:
        st.session_state[key] = "-"

# 2. Update your button to use 'on_click'
if st.button("🔄 Reset All Picks", use_container_width=True, on_click=reset_draft):
    # We don't need code inside the 'if' block anymore!
    pass

with col2:
    st.subheader("🔴 Red Side (Enemy Team)")
    red_top = st.selectbox("Red Top", ["-"] + TOP_CHAMPS, key="r_top")
    red_jng = st.selectbox("Red Jungle", ["-"] + JUNGLE_CHAMPS, key="r_jng")
    red_mid = st.selectbox("Red Mid", ["-"] + MID_CHAMPS, key="r_mid")
    red_bot = st.selectbox("Red Bot", ["-"] + BOT_CHAMPS, key="r_bot")
    red_sup = st.selectbox("Red Support", ["-"] + SUPPORT_CHAMPS, key="r_sup")

st.divider()

# --- PHASE 3: COMPUTATION ---

# Map the dropdown variables to the current session role
role_map = {
    "Top": (blue_top, red_top),
    "Jungle": (blue_jng, red_jng),
    "Mid": (blue_mid, red_mid),
    "Bot": (blue_bot, red_bot),
    "Support": (blue_sup, red_sup)
}

# This sets the 'Primary Subject' for all following calculations
my_champ, enemy_champ = role_map[user_role]

# Define who your teammates and enemies are (excluding your focal opponent)
active_blue_team = [c for c in [blue_top, blue_jng, blue_mid, blue_bot, blue_sup] if c != "-"]
active_red_team = [c for c in [red_top, red_jng, red_mid, red_bot, red_sup] if c != "-"]

# For global calculations, we need "The Others"
red_others = [e for e in active_red_team if e != enemy_champ and e != "-"]
blue_others = [a for a in active_blue_team if a != my_champ and a != "-"]



#--This is used for both Your team and the enemy team. This checks for deltas in synergy and overall matchups.--

def lookup_delta(my_champ, target_champ, dataframe):
    """
    Universal lookup for Delta values. 
    Includes the transposition check for Synergy_Matrix.
    """
    if my_champ == "-" or target_champ == "-":
        return 0.0

    my_c = str(my_champ).strip()
    target_c = str(target_champ).strip()

    # Match: My Champ (Col 1) vs Target Champ (Col 3)
    mask = (
        (dataframe.iloc[:, 1].astype(str).str.strip() == my_c) & 
        (dataframe.iloc[:, 3].astype(str).str.strip() == target_c)
    )
    row = dataframe[mask]

    # THE FIX: Transposition / Reverse Check
    if row.empty:
        mask_rev = (
            (dataframe.iloc[:, 1].astype(str).str.strip() == target_c) & 
            (dataframe.iloc[:, 3].astype(str).str.strip() == my_c)
        )
        row = dataframe[mask_rev]

    if not row.empty:
        try:
            return float(row.iloc[0, 4]) # Delta value is in Column 4
        except (ValueError, TypeError):
            return 0.0
            
    return 0.0
    
#-- Lane agnostic score for matchup data we grabbed. Now it will look for the First column of the sheet which should be the Role.-- 

def calculate_lane_score(my_champ, enemy_champ, user_role, df_matchups, df_dna):
    """
    Now it checks the first column (Role) to ensure we get the right matchup data.
    """
    if enemy_champ == "-" or enemy_champ not in df_dna['Name'].values:
        return 50.0
    
    # THE FIX: We add (df_matchups.iloc[:, 0] == user_role) to the filter
    mask = (
        (df_matchups.iloc[:, 0] == user_role) & 
        (df_matchups['My_Champ'] == my_champ) & 
        (df_matchups['Opp_Champ'] == enemy_champ)
    )
    
    matchup = df_matchups[mask]
    
    # Archetype fallback if specific matchup is missing
    if matchup.empty:
        enemy_row = df_dna[df_dna['Name'] == enemy_champ]
        if not enemy_row.empty:
            enemy_arch = enemy_row['Role_Type'].values[0]
            # Also filter fallback by role!
            mask_arch = (
                (df_matchups.iloc[:, 0] == user_role) & 
                (df_matchups['My_Champ'] == my_champ) & 
                (df_matchups['Opp_Champ'] == f"{enemy_arch}_Avg")
            )
            matchup = df_matchups[mask_arch]

    if not matchup.empty:
        wr = float(matchup['Matchup_Winrate'].values[0])
        gd = float(matchup['Gold_Delta_15'].values[0])
        xp = float(matchup['XP_Delta_15'].values[0])
        kd = float(matchup['Kill_Delta_15'].values[0])
        # Your custom formula for lane dominance
        return round(wr + (gd/100) + (xp/200) + (kd*12), 1)
    
    return 50.0
    
def get_matchup_metrics(my_champ, opp_champ, target_role, df_matchups):
    """Pulls the raw gd, xp, kd, and wr for a specific matchup."""
    # Safety net if the enemy hasn't been picked yet
    if my_champ == "-" or opp_champ == "-":
        return {'gd15': 0.0, 'xp15': 0.0, 'kd15': 0.0, 'wr': 50.0}
        
    mask = (
        (df_matchups.iloc[:, 0] == target_role) & 
        (df_matchups['My_Champ'] == my_champ) & 
        (df_matchups['Opp_Champ'] == opp_champ)
    )
    matchup = df_matchups[mask]
    
    if not matchup.empty:
        return {
            'gd15': float(matchup['Gold_Delta_15'].values[0]),
            'xp15': float(matchup['XP_Delta_15'].values[0]),
            'kd15': float(matchup['Kill_Delta_15'].values[0]),
            'wr': float(matchup['Matchup_Winrate'].values[0])
        }
    
    # Fallback if no data is found
    return {'gd15': 0.0, 'xp15': 0.0, 'kd15': 0.0, 'wr': 50.0}

# -- THIS IS A SEPARATE CALCULATION ONLY FOR BOT AND SUPPORT. WE'LL NEED TO CALL THIS SPECIFICALLY IN THE MASTER SCORE
def calculate_duo_lane_score(my_adc, my_supp, opp_adc, opp_supp, df_matchups, df_synergy):
    """Calculates the multiplicative 2v2 Lane Pressure Score."""
    # 1. Get individual data for both
    adc_data = get_matchup_metrics(my_adc, opp_adc, "Bot", df_matchups)
    supp_data = get_matchup_metrics(my_supp, opp_supp, "Support", df_matchups)
    
    # 2. Sum the Deltas (The "Shared Bucket")
    total_gd = adc_data['gd15'] + supp_data['gd15']
    total_xp = adc_data['xp15'] + supp_data['xp15']
    total_kd = adc_data['kd15'] + supp_data['kd15']
    avg_wr = (adc_data['wr'] + supp_data['wr']) / 2

    # 3. Apply the Synergy Multiplier
    synergy_delta = lookup_delta(my_adc, my_supp, df_synergy)
    multiplier = 1 + (synergy_delta / 100)

    # 4. Final Calculation
    raw_score = avg_wr + (total_gd / 100) + (total_xp / 200) + (total_kd * 12)
    unified_score = raw_score * multiplier

    return round(unified_score, 1)

# --This is a separate calculation on for Jungle. This is to do the inverse of the Gank risk scores.
def calculate_lane_gank_score(target_lane, blue_team_dict, red_team_dict, df_dna):
    """
    Calculates gank setup for a specific lane.
    Scale: 0 (Impossible) to 100 (Free Kill).
    """
    # 1. Pull the stats based on the lane
    if target_lane in ["Bot", "Support"]:
        # Handle the Duo Lane as a single unit
        # We average their CC and their Mobility
        blue_cc = (get_dna_stat(blue_team_dict['Bot'], 'CC', df_dna) + 
                   get_dna_stat(blue_team_dict['Support'], 'CC', df_dna)) / 2
        red_mob = (get_dna_stat(red_team_dict['Bot'], 'Mobility', df_dna) + 
                   get_dna_stat(red_team_dict['Support'], 'Mobility', df_dna)) / 2
    else:
        # Solo Lanes (Top/Mid)
        blue_cc = get_dna_stat(blue_team_dict[target_lane], 'CC', df_dna)
        red_mob = get_dna_stat(red_team_dict[target_lane], 'Mobility', df_dna)

    # 2. The Math: (Setup Score)
    # Start at 50 (Neutral). 
    # High Ally CC (+4 per point) | High Enemy Mobility (-4 per point)
    setup_score = 50 + (blue_cc * 4) - (red_mob * 4)
    
    return max(0, min(100, round(setup_score, 1)))


def calculate_scaling_fit(my_champ, team_selections, df_dna):
    my_dna_row = df_dna[df_dna['Name'] == my_champ]
    if my_dna_row.empty: return 75
        
    my_dna = my_dna_row.iloc[0]
    my_curve = {'E': my_dna['Scaling_E'], 'M': my_dna['Scaling_M'], 'L': my_dna['Scaling_L']}
    
    team_dna = df_dna[df_dna['Name'].isin(team_selections)]
    if team_dna.empty:
        team_avg = {'E': 2.0, 'M': 2.0, 'L': 2.0}
    else:
        team_avg = {'E': team_dna['Scaling_E'].mean(), 'M': team_dna['Scaling_M'].mean(), 'L': team_dna['Scaling_L'].mean()}

    fit_score = 0
    for phase in ['E', 'M', 'L']:
        if team_avg[phase] < 1.8 and my_curve[phase] == 3: fit_score += 35
        elif team_avg[phase] > 2.4 and my_curve[phase] == 3: fit_score += 10 
        else: fit_score += 25
    return min(fit_score, 100)
    
#--Does  a calculation of the Damage composition of our team. I should think about using this for both teams eventually to alert the user of the need for Armor/the like but we can do that later--

def calculate_dmg_diversity(my_champ, team_selections, df_dna):
    my_dna_row = df_dna[df_dna['Name'] == my_champ]
    if my_dna_row.empty: return 75
        
    my_dna = my_dna_row.iloc[0]
    team_dna = df_dna[df_dna['Name'].isin(team_selections)]
    
    if not team_dna.empty:
        # UPDATED HEADERS
        team_ad_points = (team_dna['Dmg%_Atk'] * team_dna['Dmg_Intensity']).sum()
        team_ap_points = (team_dna['Dmg%_Mag'] * team_dna['Dmg_Intensity']).sum()
        total_intensity = team_dna['Dmg_Intensity'].sum()
        
        team_ad = (team_ad_points / total_intensity) if total_intensity > 0 else 50.0
        team_ap = (team_ap_points / total_intensity) if total_intensity > 0 else 50.0
    else:
        team_ad, team_ap = 50.0, 50.0

    # UPDATED HEADERS
    my_ad, my_ap, my_true = my_dna['Dmg%_Atk'], my_dna['Dmg%_Mag'], my_dna['Dmg%_True']
    
    diversity_score = 75
    
    # 1. Penalty: If the team is already AD heavy and you are ALSO high AD
    if team_ad > 70 and my_ad > 70: 
        # True damage reduces the penalty because it can't be resisted by Armor
        penalty = 40 - (my_true * 0.5)
        diversity_score -= penalty
        
    # 2. Penalty: If the team is AP heavy and you are ALSO high AP
    elif team_ap > 70 and my_ap > 70: 
        penalty = 40 - (my_true * 0.5)
        diversity_score -= penalty
        
    # 3. Bonus: If you provide the missing damage type (e.g., Team is AD, you are AP)
    elif team_ad > 70 and (my_ap + my_true) > 50: 
        diversity_score += 25
    elif team_ap > 70 and (my_ad + my_true) > 50:
        diversity_score += 25

    return min(max(diversity_score, 0), 100)
    
#This calculates our risk of being ganked by the enemy team. Not how likely are they to, but how effective the gank could be if done correctly.
#We'll need a secondary one for Botlane and Support but this works for Mid and Toplane.

def calculate_gank_risk(my_champ, enemy_champ, red_jng, df_dna):
    # Check if either of the relevant threats is missing
    if red_jng == "-" or enemy_champ == "-" or red_jng not in df_dna['Name'].values:
        return "Unknown"
        
    my_stats = df_dna[df_dna['Name'] == my_champ].iloc[0]
    jng_stats = df_dna[df_dna['Name'] == red_jng].iloc[0]
    opp_stats = df_dna[df_dna['Name'] == enemy_champ].iloc[0]
    
    # Combined pressure of the Lane Opponent + the Jungler
    enemy_kill_pressure = (jng_stats['Control(CC)'] + jng_stats['Dmg_Intensity']) + \
                          (opp_stats['Control(CC)'] + opp_stats['Dmg_Intensity'])
    
    # Your ability to survive (Running away vs. Tanking it)
    my_defense = my_stats['Mobility'] + my_stats['Toughness']
    
    risk_delta = enemy_kill_pressure - my_defense
    
    if risk_delta >= 6: return "🔴 EXTREME"
    if risk_delta >= 4: return "🟠 High"
    if risk_delta <= 1: return "🟢 Low"
    return "🟡 Moderate"
    
    #--calculates the synergy between your jungle and the enemy and their jungle. This allows you to see if you win the 2v2 in general or not.

def assess_2v2_threat(enemy_champ, red_jng, my_syn_delta, df_synergy):
    # Check for empty slots
    if enemy_champ == "-" or red_jng == "-": 
        return 0.0
    
    # 1. Look up how well the enemy laner and enemy jungler play together
    enemy_delta = lookup_delta(enemy_champ, red_jng, df_synergy)
    
    # 2. Compare their synergy "score" against yours with your jungler
    # A positive number means they have a synergy advantage.
    # A negative number means your duo has the synergy advantage.
    return round(enemy_delta - my_syn_delta, 2)
    
#--The next 2 give us recommendatiosn on blind picks based on our pool 
    
def get_blind_pick_average(my_champ, user_role, df_matchups):
    # Filter by the first column (Role) AND your champ
    matchups = df_matchups[
        (df_matchups.iloc[:, 0] == user_role) & 
        (df_matchups['My_Champ'] == my_champ)
    ].copy()
    
    if matchups.empty: return 50.0
    
    matchups['Matchup_Winrate'] = pd.to_numeric(matchups['Matchup_Winrate'], errors='coerce')
    # Now it only averages the worst 10 matchups YOU will actually face in that lane
    worst_10 = matchups.sort_values(by='Matchup_Winrate', ascending=True).head(10)
    return round(worst_10['Matchup_Winrate'].mean(), 2)

def get_best_blind_picks(my_pool, user_role, df_matchups, top_n=2):
    """Evaluates the pool and returns the top N champions with the highest 'worst-case' floor."""
    blind_scores = []
    for champ in my_pool:
        # Pass user_role here too so the average is role-specific!
        score = get_blind_pick_average(champ, user_role, df_matchups)
        blind_scores.append((champ, score))
    
    blind_scores.sort(key=lambda x: x[1], reverse=True)
    return blind_scores[:top_n]

#--Gives us the overall calculation we use to see how strong our score is in comparison to other choices in our pool. Thing is eventually I want to make sure this has different weightings for the different roles--

def calculate_master_score(my_champ, Opp_champ, user_role, blue_team_list, red_team_list, 
                           df_matchups, df_dna, df_synergy, df_globalmatchups, 
                           blue_bot, blue_sup, red_bot, red_sup, 
                           archetype_key="Standard", gank_score=50):
    """
    Revised Master Score calculation with Dynamic Weighting and Duo-Synergy protection.
    """
    # 0. Fetch the correct weights from our dictionary
    weights = WEIGHTING_PROFILES.get(archetype_key, WEIGHTING_PROFILES["Standard"])

    # 1. Lane Score Routing
    if user_role in ["Bot", "Support"]:
        # Activate the 2v2 Unified Engine
        lane_score = calculate_duo_lane_score(blue_bot, blue_sup, red_bot, red_sup, df_matchups, df_synergy)
    else:
        # Standard Solo Lane Engine
        lane_score = calculate_lane_score(my_champ, Opp_champ, user_role, df_matchups, df_dna)
    
    # 2. Global Enemy Counter
    other_enemies = [e for e in red_team_list if e != Opp_champ]
    total_enemy_delta = 0.0
    for enemy in other_enemies:
        if enemy != "-":
            total_enemy_delta += lookup_delta(my_champ, enemy, df_globalmatchups)
    
    enemy_counter_score = 50 + (total_enemy_delta * 10)
    
    # 3. Global Team Synergy (With Double-Dip Fix)
    total_synergy_delta = 0.0
    for ally in blue_team_list:
        if ally == "-" or ally == my_champ:
            continue
        
        # --- THE DOUBLE-DIP FIX ---
        # If we are in a duo lane, skip the partner because their synergy 
        # is already calculated in the 'lane_score' above.
        if user_role == "Bot" and ally == blue_sup:
            continue
        if user_role == "Support" and ally == blue_bot:
            continue
            
        total_synergy_delta += lookup_delta(my_champ, ally, df_synergy)
            
    synergy_score = 50 + (total_synergy_delta * 10)
    
    # 4. Scaling & Damage
    scaling_score = calculate_scaling_fit(my_champ, blue_team_list, df_dna)
    dmg_score = calculate_dmg_diversity(my_champ, blue_team_list, df_dna)
    
    # 5. FINAL WEIGHTED CALCULATION
    # The 'gank' component will naturally zero out for non-junglers based on the dictionary.
    ms = (lane_score * weights["lane"]) + \
         (enemy_counter_score * weights["counter"]) + \
         (synergy_score * weights["synergy"]) + \
         (scaling_score * weights["scaling"]) + \
         (dmg_score * weights["damage"]) + \
         (gank_score * weights["gank"])
    
    return round(ms, 1)
    
#--used to give us our recommnded bans

def identify_overlapping_threats(my_pool, df_matchups, role_base_df, current_role):
    # --- DEFENSIVE CODING: Fallback if header names change ---
    LANE_COLUMN = 'My_Lane' if 'My_Lane' in df_matchups.columns else 'Lane'
    CHAMP_COL = 'My_Champ'
    WR_COL = 'Matchup_Winrate'
    # --- DYNAMIC ROLE: Use the sidebar selection instead of 'Top' ---
    LANE_VALUE = current_role

    # 1. Setup Base Winrates
    role_base_df_clean = role_base_df.copy()
    
    # Target columns by name so the order doesn't matter
    # Ensure 'Champion' and 'Winrate' match your Google Sheet headers exactly
    role_base_df_clean['Win Rate'] = pd.to_numeric(role_base_df_clean['Win Rate'], errors='coerce').fillna(50.0)
    
    # Create the map using names: { "Kled": 52.1, "Gwen": 49.5 }
    base_wr_map = dict(zip(role_base_df_clean['Champion'], role_base_df_clean['Win Rate']))

    # 2. Filter for Pool and Lane, then Deduplicate
    pool_matchups = df_matchups[
        (df_matchups['My_Champ'].isin(my_pool)) & 
        (df_matchups[LANE_COLUMN] == LANE_VALUE)
    ].copy()
    pool_matchups = pool_matchups.drop_duplicates(subset=['My_Champ', 'Opp_Champ'])
    pool_matchups['Matchup_Winrate'] = pd.to_numeric(pool_matchups['Matchup_Winrate'], errors='coerce')
    
    # Calculate Delta for Z
    pool_matchups['WR_Delta'] = pool_matchups.apply(
        lambda row: row['Matchup_Winrate'] - base_wr_map.get(row['My_Champ'], 50.0), 
        axis=1
    )

    # 3. Identify Top 15 Worst Matchups per Champion (The "X" Factor)
    top_15_lists = []
    for champ in my_pool:
        champ_matchups = pool_matchups[pool_matchups['My_Champ'] == champ]
        # Grab the 15 lowest absolute winrates for this specific champion
        worst_15 = champ_matchups.nsmallest(15, 'Matchup_Winrate')
        top_15_lists.append(worst_15)

    # Combine all Top 15 lists into one dataframe
    top_15_df = pd.concat(top_15_lists)

    # Calculate X: How many Top 15 lists does this enemy appear in?
    x_counts = top_15_df.groupby('Opp_Champ').size().reset_index(name='X_Top15_Count')

    # 4. Calculate Y & Z against the ENTIRE pool
    agg_stats = pool_matchups.groupby('Opp_Champ').agg(
        # Y: How many champions do they ACTUALLY beat? (Winrate strictly < 50%)
        Y_Losing_Matchups=('Matchup_Winrate', lambda w: (w < 50.0).sum()),
        # Z: What is the average delta reduction?
        Z_Avg_Delta=('WR_Delta', 'mean')
    ).reset_index()

    # 5. Merge and Rank
    threats = pd.merge(x_counts, agg_stats, on='Opp_Champ', how='left')

    # Optional: Filter out noise (only show champions that appear in at least 2 Top 15 lists)
    # If a champion only counters 1 of your picks, it's not a "systemic" threat.
    threats = threats[threats['X_Top15_Count'] >= 2]

    # Sort strictly by your rules: X (highest), then Y (highest), then Z (lowest/most negative)
    threats = threats.sort_values(
        by=['X_Top15_Count', 'Y_Losing_Matchups', 'Z_Avg_Delta'], 
        ascending=[False, False, True]
    )

    return threats
    
# --- PHASE 4: RECOMMENDATION UI ---
st.subheader("📊 Live Recommendations")

blue_others = [c for c in [blue_top, blue_jng, blue_mid, blue_bot, blue_sup] if c != "-" and c != my_champ]
red_others = [c for c in [red_top, red_jng, red_mid, red_bot, red_sup] if c != "-" and c != enemy_champ]

blue_team_current = [c for c in [blue_top, blue_jng, blue_mid, blue_bot, blue_sup] if c != "-"]

# --- NEW: BLIND PICK & BAN BANNER ---
# This banner ONLY shows if the enemy laner is unpicked.
if enemy_champ == "-":
    st.info(f"Enemy {user_role} is Unknown. Baseline Lane Score set to 50.0. Use Blind Pick metrics.")
    
    bp1, bp2 = st.columns(2)
    with bp1:
        st.write("🛡️ **Safest Blind Picks (Highest Floor)**")
        best_blinds = get_best_blind_picks(my_pool, user_role, df_matchups, top_n=2)
        for rank, (champ, wr) in enumerate(best_blinds):
            st.caption(f"{rank+1}. **{champ}** (Worst 10 Avg: {wr}%)")
            
    with bp2:
        st.write("🚫 **Systemic Ban Recommendations**")

        current_role_df = ROLE_DF_MAP.get(user_role)

        if current_role_df is not None and len(my_pool) > 0:
            # Pass 'user_role' as the new fourth argument
            threats_df = identify_overlapping_threats(my_pool, df_matchups, current_role_df, user_role)
        
            if not threats_df.empty:
                # Grab the top 3 threats for the UI
                top_threats = threats_df.head(3)
                primary_ban = top_threats.iloc[0]['Opp_Champ']
                
                # Highlight the absolute worst matchup
                st.error(f"**PRIMARY BAN: {primary_ban}**")
                st.caption("Alternative bans available if a teammate hovers this champion.")
                
                # Loop through the top 3 to display the specific X, Y, Z breakdown
                for rank, (_, row) in enumerate(top_threats.iterrows()):
                    champ_name = row['Opp_Champ']
                    x = int(row['X_Top15_Count'])
                    y = int(row['Y_Losing_Matchups'])
                    z = round(row['Z_Avg_Delta'], 2)

                    # The first expander stays open, the alternates stay closed to save space
                    with st.expander(f"#{rank+1} Threat: {champ_name}", expanded=(rank == 0)):
                        st.write(
                            f"**{champ_name}** is in the Top 15 worst matchups for **{x}** champions in your pool. "
                            f"They have a winning matchup against **{y}** champions, and reduce your overall win percentage by **{abs(z)}%**."
                        )
            else:
                st.success("Your current pool is incredibly well-rounded. No systemic vulnerabilities detected.")
        else:
            st.caption("Add champions to your pool to analyze vulnerabilities.")
        
        st.divider()

# --- 1. CHAMPION CARDS SECTION ---
if len(my_pool) > 0:
    cols = st.columns(len(my_pool))

    # Define team context once
    blue_team_dict = {
        "Top": blue_top, "Jungle": blue_jng, "Mid": blue_mid, "Bot": blue_bot, "Support": blue_sup
    }
    red_team_dict = {
        "Top": red_top, "Jungle": red_jng, "Mid": red_mid, "Bot": red_bot, "Support": red_sup
    }

    for i, champ in enumerate(my_pool):
        with cols[i]:
            # --- INITIALIZE DEFAULTS (Prevents NameErrors) ---
            archetype_key = "Standard"
            gank_top, gank_mid, gank_bot = 50.0, 50.0, 50.0
            avg_gank_score = 50.0 

            # --- JUNGLE SPECIFIC LOGIC ---
            if user_role == "Jungle":
                # 1. Determine Archetype
                farmer_check = df_meta.loc[
                    (df_meta['Champion'] == champ) & (df_meta['Role'] == 'Jungle'), 
                    'Power Farmer'
                ].values
                
                if len(farmer_check) > 0 and farmer_check[0] == 'X':
                    archetype_key = "Jungle_Farmer"
                else:
                    archetype_key = "Jungle_Ganker"

                # 2. Calculate Gank Potentials
                gank_top = calculate_lane_gank_score("Top", blue_team_dict, red_team_dict, df_dna)
                gank_mid = calculate_lane_gank_score("Mid", blue_team_dict, red_team_dict, df_dna)
                gank_bot = calculate_lane_gank_score("Bot", blue_team_dict, red_team_dict, df_dna)
                
                avg_gank_score = (gank_top + gank_mid + gank_bot) / 3

            # --- 3. CALCULATIONS (Master Score) ---
            # Now all variables are guaranteed to exist
            ms_value = calculate_master_score(
                champ, 
                enemy_champ, 
                user_role,
                blue_team_current,
                red_others, 
                df_matchups, 
                df_dna, 
                df_synergy, 
                df_globalmatchups,
                blue_bot, 
                blue_sup, 
                red_bot, 
                red_sup,
                archetype_key=archetype_key,
                gank_score=avg_gank_score
            )
            
            # --- 3. SYNERGY & THREATS ---
            primary_synergy_target = blue_mid if user_role == "Jungle" else blue_jng
            syn_delta = lookup_delta(champ, primary_synergy_target, df_synergy)
            
            threat_diff = assess_2v2_threat(enemy_champ, red_jng, syn_delta, df_synergy) 
            gank_risk = calculate_gank_risk(champ, enemy_champ, red_jng, df_dna) 
    
            lane_val = calculate_lane_score(champ, enemy_champ, user_role, df_matchups, df_dna)
            lane_delta = round(lane_val - 50, 1)
    
            # --- 4. UI METRICS ---
            st.metric(
                label=f"{champ} MS", 
                value=f"{ms_value}", 
                delta=f"{lane_delta} Lane"
            )
    
            if ms_value >= 65: st.success("🏆 OPTIMAL")
            elif ms_value >= 55: st.info("✅ VIABLE")
            else: st.warning("⚠️ SITUATIONAL")

            # --- 5. TACTICAL CAPTIONS ---
            if enemy_champ == "-":
                blind_score = get_blind_pick_average(champ, user_role, df_matchups)
                st.caption(f"🫣 **Blind Floor:** {blind_score}%")
            
            # JUNGLE VIEW: Pathing and Lane Gank Potential
            if user_role == "Jungle":
                st.write("---")
                st.caption("📍 **Lane Gank Potential**")

                # Use color-coding for quick reading
                def color_val(v):
                    if v >= 65: return "green"
                    if v <= 35: return "red"
                    return "gray"

                st.markdown(f":{color_val(gank_top)}[**TOP:** {gank_top}]")
                st.markdown(f":{color_val(gank_mid)}[**MID:** {gank_mid}]")
                st.markdown(f":{color_val(gank_bot)}[**BOT:** {gank_bot}]")

                # 5. Add a simple pathing recommendation
                if gank_top > gank_bot + 15:
                    st.caption("💡 *Advice: Stronger Setup Top*")
                elif gank_bot > gank_top + 15:
                    st.caption("💡 *Advice: Stronger Setup Bot*")
                elif gank_mid > 65:
                    st.caption("💡 *Advice: High Priority Mid Gank*")
            else:
                if gank_risk != "Unknown":
                    st.caption(f"🛡️ Gank Risk: {gank_risk}")
            
                if primary_synergy_target != "-":
                    if syn_delta >= 1.5: st.success(f"🔥 **SYNERGY:** +{syn_delta}%")
                    elif syn_delta <= -1.5: st.error(f"❄️ **BAD SYNERGY:** {syn_delta}%")
                    else: st.caption(f"🤝 Neutral Synergy ({syn_delta}%)")
            
                if threat_diff != 0:
                    if threat_diff > 1.5: st.caption(f"🚨 **2v2 Danger:** Enemy +{threat_diff}%")
                    elif threat_diff < -1.5: st.caption(f"⚔️ **2v2 Gap:** You +{abs(threat_diff)}%")

else:
    st.info("No champions selected in your pool. Use the sidebar to add picks.")

st.divider()

    # 2. GLOBAL DRAFT ALERTS (The "Safety Net")
st.subheader("💡 Strategic Insights")
    
current_comp = blue_team_current

if current_comp:
    t_dna = df_dna[df_dna['Name'].isin(current_comp)].copy()
    
    if not t_dna.empty:
        # --- A. Scaling Curve Alert ---
        avg_e = t_dna['Scaling_E'].mean()
        avg_l = t_dna['Scaling_L'].mean()

        if pd.notnull(avg_e) and pd.notnull(avg_l):
            if avg_e > 2.6:
                st.error("🚨 **EARLY GAME OVERLOAD:** Win by 20m. Force dives and objectives.")
            elif avg_l > 2.6:
                st.warning("🐢 **SCALING DELAY:** Weak early. Give up early drakes to hit power spikes.")

        # --- B. Intensity-Weighted Damage Profile Alert ---
        if len(current_comp) >= 2:
            # Calculate total 'Damage Influence Points'
            # (Damage % * Intensity)
            weighted_ad = (t_dna['Dmg%_Atk'] * t_dna['Dmg_Intensity']).sum()
            weighted_ap = (t_dna['Dmg%_Mag'] * t_dna['Dmg_Intensity']).sum()
            
            # The divisor is the sum of all intensities in the current team
            total_intensity_pool = t_dna['Dmg_Intensity'].sum()

            if total_intensity_pool > 0:
                # Calculate the weighted impact percentage
                true_ad_impact = weighted_ad / total_intensity_pool
                true_ap_impact = weighted_ap / total_intensity_pool

                # Thresholds: If a specific damage type makes up >75% of the team's 'Threat'
                if true_ad_impact > 75:
                    st.error(f"⚔️ **PHYSICAL HEAVY ({true_ad_impact:.0f}%):** High-intensity AD threat. Enemy will stack Armor. Need AP/True damage.")
                elif true_ap_impact > 75:
                    st.error(f"🔮 **MAGIC HEAVY ({true_ap_impact:.0f}%):** High-intensity AP threat. Enemy will stack MR. Ensure %HP or Void Staff.")
                else:
                    st.success(f"⚖️ **BALANCED DAMAGE:** AD: {true_ad_impact:.0f}% | AP: {true_ap_impact:.0f}%")
        else:
            st.caption("Add more teammates to analyze team damage balance.")
    else:
        st.write("Awaiting DNA data for selected champions...")
    
# --- PHASE 5: FINAL DRAFT SUMMARY ---
st.header("📋 Pre-Game Tactical Briefing")

active_blue_team = [c for c in [blue_top, blue_jng, blue_mid, blue_bot, blue_sup] if c != "-"]

# Main Check: Only run if your champion is selected
if my_champ != "-":
    final_lane_score = calculate_lane_score(my_champ, enemy_champ, user_role, df_matchups, df_dna)
    
    # If you are Jungle, the "Gank Risk" logic might need to be inverted or looking at enemy mid/jng
    # For lane roles, this works:
    enemy_jungle_threat = red_mid if user_role == "Jungle" else red_jng 
    combined_gank_threat = calculate_gank_risk(my_champ, enemy_champ, enemy_jungle_threat, df_dna)
    
    t_dna = df_dna[df_dna['Name'].isin(active_blue_team)]
    avg_e = t_dna['Scaling_E'].mean() if not t_dna.empty else 2.0
    avg_l = t_dna['Scaling_L'].mean() if not t_dna.empty else 2.0

    # --- NEW FIX 1: PULL THE RAW LANE STATS ---
    matchup = df_matchups[
        (df_matchups.iloc[:, 0] == user_role) & 
        (df_matchups['My_Champ'] == my_champ) & 
        (df_matchups['Opp_Champ'] == enemy_champ)
    ]
    
    if not matchup.empty:
        gd = float(matchup['Gold_Delta_15'].values[0])
        xp = float(matchup['XP_Delta_15'].values[0])
        kd = float(matchup['Kill_Delta_15'].values[0])
    else:
        gd, xp, kd = 0, 0, 0

    # Logic to simplify deltas into status codes
    g_status = 1 if gd > 400 else (-1 if gd < -400 else 0)
    x_status = 1 if xp > 400 else (-1 if xp < -400 else 0)
    k_status = 1 if kd > 0.5 else (-1 if kd < -0.5 else 0)

    # Filter the df_lane_logic sheet to find the exact match
    lane_match = df_lane_logic[
        (df_lane_logic['Gold_Delta (G)'] == g_status) &
        (df_lane_logic['XP_Delta (X)'] == x_status) &
        (df_lane_logic['Kill_Delta (K)'] == k_status)
    ]

    # Pull the narrative and format it into two lines
    if not lane_match.empty:
        l_title = str(lane_match['Archetype_Title'].values[0]).strip()
        l_body = str(lane_match['Advice_Body'].values[0]).strip()
        # This formatting gives you the Title in bold, followed by a line break, then the Body
        briefing_text = f"**{l_title}**\n\n{l_body}"
    else:
        briefing_text = "Intel Unavailable."
    
    # --- NEW FIX 2: PULL THE SCALING TRAJECTORY ---
    my_dna = df_dna[df_dna['Name'] == my_champ]
    opp_dna = df_dna[df_dna['Name'] == enemy_champ]

    if not my_dna.empty and not opp_dna.empty and red_top != "-":
        e_delta = int(my_dna['Scaling_E'].values[0] - opp_dna['Scaling_E'].values[0])
        m_delta = int(my_dna['Scaling_M'].values[0] - opp_dna['Scaling_M'].values[0])
        l_delta = int(my_dna['Scaling_L'].values[0] - opp_dna['Scaling_L'].values[0])
        
        # Filter the df_scaling_logic sheet to find the exact match
        scale_match = df_scaling_logic[
            (df_scaling_logic['Early_Strength_Delta'] == e_delta) &
            (df_scaling_logic['Mid_Strength_Delta'] == m_delta) &
            (df_scaling_logic['Late_Strength_Delta'] == l_delta)
        ]
        
        # Pull the narrative and format it into two lines
        if not scale_match.empty:
            s_title = str(scale_match['Archetype_Name'].values[0]).strip()
            s_body = str(scale_match['Advice_Body'].values[0]).strip()
            trajectory_text = f"**{s_title}**\n\n{s_body}"
        else:
            trajectory_text = "Trajectory Analysis Offline."
    else:
        trajectory_text = "Awaiting Enemy Matchup to forecast scaling."

    # --- RENDER THE COLUMNS ---
    b1, b2, b3 = st.columns(3)

    with b1:
        st.write("**Laning Dynamics**")
        if enemy_champ == "-":
            st.info("Awaiting Enemy Matchup...")
        else:
            # Check the status to decide the color
            total_status = g_status + x_status + k_status
            if total_status >= 2:
                st.success(briefing_text)
            elif total_status <= -2:
                st.error(briefing_text)  
            else:
                st.info(briefing_text)
    
    with b2:
        st.write("**Gank Survival**")
        if combined_gank_threat == "Unknown":
            st.info("Awaiting Enemy Jungle Data...")
        elif "EXTREME" in combined_gank_threat or "High" in combined_gank_threat:
            st.error(f"WATCH FOR THE DIVE\n\nThreat: {combined_gank_threat}")
        else:
            st.success(f"SAFE TO AGGRESS\n\nThreat: {combined_gank_threat}")

    with b3:
        st.write("**Win Condition**")
        if avg_e > 2.6: 
            st.warning("⏱️ EARLY TEMPO")
        elif avg_l > 2.6: 
            st.info("💎 LATE SCALING")
        else: 
            st.success("⚖️ BALANCED")
            
        st.markdown("**Tactical Forecast:**")
        st.caption(trajectory_text)

else:
    st.info(f"Lock in your {user_role} pick to see your tactical briefing.")
