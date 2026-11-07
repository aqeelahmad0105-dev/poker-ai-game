import os
import sys
import time
import uuid
import random
import itertools
from collections import Counter
import joblib
import numpy as np
import pandas as pd
import streamlit as st

# ==============================================================================
# STREAMLIT PAGE CONFIGURATION
# ==============================================================================
st.set_page_config(
    page_title="Texas Hold'em Multiplayer AI Championship",
    page_icon="♠️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==============================================================================
# RESPONSIVE CASINO POKER CSS STYLING (Mobile, Tablet & Desktop)
# ==============================================================================
POKER_CSS = """
<style>
/* App Dark Casino Theme */
.stApp {
    background: radial-gradient(circle at 50% 20%, #152433 0%, #0a1118 100%);
    color: #ffffff;
    font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
}

/* Page container padding */
.block-container {
    padding-top: 1.2rem !important;
    padding-bottom: 2rem !important;
    padding-left: 1rem !important;
    padding-right: 1rem !important;
    max-width: 1300px;
}

/* Casino Felt Oval Table (Desktop Default) */
.felt-table {
    background: radial-gradient(ellipse at 50% 45%, #188651 0%, #0f5b36 60%, #0a3d24 100%);
    border: 14px solid #42250f;
    border-radius: 160px;
    box-shadow: inset 0 0 50px rgba(0,0,0,0.85), 0 12px 35px rgba(0,0,0,0.9);
    padding: 22px 16px;
    margin: 8px auto 16px auto;
    position: relative;
    max-width: 1040px;
    width: 100%;
    box-sizing: border-box;
}

/* Inner gold line on felt */
.felt-table::before {
    content: "";
    position: absolute;
    top: 12px; left: 12px; right: 12px; bottom: 12px;
    border: 2px dashed rgba(255, 215, 0, 0.35);
    border-radius: 140px;
    pointer-events: none;
}

/* Centered Pot Container */
.pot-container {
    text-align: center;
    margin: 4px 0 8px 0;
}
.pot-chip-pill {
    background: linear-gradient(180deg, #ffd700 0%, #d4af37 50%, #996515 100%);
    color: #0b1015;
    font-weight: 900;
    font-size: 18px;
    padding: 5px 20px;
    border-radius: 30px;
    display: inline-block;
    box-shadow: 0 4px 16px rgba(255, 215, 0, 0.45);
    border: 2px solid #fff8dc;
    letter-spacing: 1px;
}

/* Realistic Poker Playing Cards (Desktop Default) */
.poker-card {
    display: inline-block;
    width: 56px;
    height: 82px;
    background: #ffffff;
    border-radius: 7px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.5);
    border: 1px solid #d4d4d4;
    padding: 3px 5px;
    margin: 0 2px;
    position: relative;
    font-family: Arial, sans-serif;
    user-select: none;
    vertical-align: middle;
    box-sizing: border-box;
}
.card-red { color: #e74c3c !important; }
.card-black { color: #1e272e !important; }

.c-corner-top {
    font-size: 12px;
    font-weight: 900;
    line-height: 1.0;
    text-align: left;
}
.c-center-suit {
    font-size: 24px;
    text-align: center;
    line-height: 1.0;
    margin-top: 8px;
}
.c-corner-bot {
    font-size: 12px;
    font-weight: 900;
    line-height: 1.0;
    text-align: right;
    position: absolute;
    bottom: 3px;
    right: 5px;
}

/* Face Down Casino Card Back */
.card-back-casino {
    background: repeating-linear-gradient(
        45deg,
        #1e3799,
        #1e3799 5px,
        #0c2461 5px,
        #0c2461 10px
    ) !important;
    border: 2px solid #ffffff !important;
    box-shadow: 0 3px 8px rgba(0,0,0,0.6) !important;
}

/* Empty Community Card Slot */
.card-slot-empty {
    display: inline-block;
    width: 56px;
    height: 82px;
    background: rgba(0, 0, 0, 0.25);
    border-radius: 7px;
    border: 2px dashed rgba(255, 215, 0, 0.4);
    margin: 0 2px;
    vertical-align: middle;
    box-sizing: border-box;
}

/* Player Seat Pods */
.player-pod {
    background: rgba(13, 24, 33, 0.92);
    border: 2px solid #233748;
    border-radius: 12px;
    padding: 7px 9px;
    text-align: center;
    box-shadow: 0 4px 12px rgba(0,0,0,0.4);
    margin: 3px;
    min-width: 110px;
    box-sizing: border-box;
}
.pod-active {
    border-color: #f1c40f !important;
    box-shadow: 0 0 16px rgba(241, 196, 15, 0.8) !important;
}
.pod-hero {
    border: 3px solid #2ecc71 !important;
    background: rgba(16, 43, 28, 0.95) !important;
    box-shadow: 0 0 16px rgba(46, 204, 113, 0.45) !important;
}
.pod-folded {
    opacity: 0.38;
    filter: grayscale(80%);
    border-color: #7f8c8d !important;
}

/* Dealer Button Puck */
.dealer-puck {
    background: #ffd700;
    color: #111;
    font-weight: 900;
    font-size: 11px;
    border-radius: 50%;
    width: 19px;
    height: 19px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 2px 6px rgba(0,0,0,0.5);
    border: 1px solid #fff;
    margin-right: 4px;
}

/* Hand Strength & Win Probability HUD */
.hud-card {
    background: rgba(13, 27, 39, 0.92);
    border: 2px solid #34495e;
    border-radius: 12px;
    padding: 12px 16px;
    margin: 8px 0 14px 0;
    box-shadow: 0 6px 16px rgba(0,0,0,0.4);
}
.prob-bar-bg {
    background: #2c3e50;
    border-radius: 10px;
    height: 16px;
    width: 100%;
    overflow: hidden;
    margin: 7px 0;
    border: 1px solid #4a627a;
}
.prob-bar-fill {
    height: 100%;
    border-radius: 10px;
    transition: width 0.3s ease;
}

/* Badges */
.badge-rf { background: #2980b9; color: white; padding: 2px 5px; border-radius: 5px; font-size: 10px; font-weight: bold; }
.badge-dqn { background: #d35400; color: white; padding: 2px 5px; border-radius: 5px; font-size: 10px; font-weight: bold; }
.badge-human { background: #27ae60; color: white; padding: 2px 5px; border-radius: 5px; font-size: 10px; font-weight: bold; }

/* Clean Minimalist Loading Spinner */
.stSpinner > div {
    border-top-color: #ffd700 !important;
}

/* Hide technical error tracebacks and internal module status widgets */
[data-testid="stException"], 
[data-testid="stStatusWidget"],
.stAppDeployButton,
header[data-testid="stHeader"] {
    display: none !important;
}

/* ==============================================================================
   RESPONSIVE DESIGN RULES FOR MOBILE & TABLET
   ============================================================================== */
@media screen and (max-width: 768px) {
    .block-container {
        padding-left: 0.25rem !important;
        padding-right: 0.25rem !important;
        padding-top: 0.5rem !important;
    }
    .felt-table {
        border-radius: 40px !important;
        padding: 10px 4px !important;
        border-width: 8px !important;
        margin: 4px auto 12px auto !important;
    }
    .felt-table::before {
        top: 6px !important; left: 6px !important; right: 6px !important; bottom: 6px !important;
        border-radius: 32px !important;
    }
    .poker-card {
        width: 38px !important;
        height: 56px !important;
        padding: 2px 2px !important;
        margin: 0 1px !important;
        border-radius: 4px !important;
    }
    .c-corner-top {
        font-size: 9px !important;
    }
    .c-center-suit {
        font-size: 16px !important;
        margin-top: 4px !important;
    }
    .c-corner-bot {
        font-size: 9px !important;
        bottom: 2px !important;
        right: 3px !important;
    }
    .card-slot-empty {
        width: 38px !important;
        height: 56px !important;
        border-radius: 4px !important;
        margin: 0 1px !important;
    }
    .player-pod {
        padding: 4px 5px !important;
        min-width: 68px !important;
        max-width: 100px !important;
        margin: 2px !important;
        border-radius: 8px !important;
        font-size: 10px !important;
    }
    .dealer-puck {
        width: 14px !important;
        height: 14px !important;
        font-size: 8px !important;
    }
    .pot-chip-pill {
        font-size: 13px !important;
        padding: 3px 12px !important;
    }
    .badge-rf, .badge-dqn, .badge-human {
        font-size: 8px !important;
        padding: 1px 3px !important;
    }
    .hud-card {
        padding: 10px 12px !important;
        margin: 6px 0 !important;
    }
}

@media screen and (min-width: 769px) and (max-width: 1024px) {
    .felt-table {
        border-radius: 90px !important;
        padding: 16px 10px !important;
        border-width: 10px !important;
    }
    .poker-card {
        width: 48px !important;
        height: 70px !important;
    }
    .card-slot-empty {
        width: 48px !important;
        height: 70px !important;
    }
    .player-pod {
        padding: 6px 8px !important;
        min-width: 95px !important;
        font-size: 12px !important;
    }
}
</style>
"""
st.html(POKER_CSS)

# ==============================================================================
# CARD DECK & EVALUATOR ENGINE
# ==============================================================================
SUIT_SYMBOLS = {'s': '♠', 'h': '♥', 'd': '♦', 'c': '♣'}
RANK_NAMES = {2:'2', 3:'3', 4:'4', 5:'5', 6:'6', 7:'7', 8:'8', 9:'9', 10:'10', 11:'J', 12:'Q', 13:'K', 14:'A'}
REV_SUIT_MAP = {'c':0, 'd':1, 'h':2, 's':3}

class Card:
    def __init__(self, rank, suit):
        self.rank = rank  # 2..14
        self.suit = suit  # 's', 'h', 'd', 'c'

    def __getitem__(self, idx):
        if idx == 0:
            return self.rank
        elif idx == 1:
            return self.suit
        raise IndexError(f"Card index {idx} out of range")

    def __iter__(self):
        yield self.rank
        yield self.suit

    def __len__(self):
        return 2

    def __repr__(self):
        return f"Card({self.rank}, '{self.suit}')"

    def to_html(self, hidden=False):
        if hidden:
            return '<div class="poker-card card-back-casino"></div>'
        r_str = RANK_NAMES.get(self.rank, str(self.rank))
        s_sym = SUIT_SYMBOLS.get(self.suit, self.suit)
        c_class = "card-red" if self.suit in ['h', 'd'] else "card-black"
        return f'<div class="poker-card {c_class}"><div class="c-corner-top">{r_str} {s_sym}</div><div class="c-center-suit">{s_sym}</div><div class="c-corner-bot">{r_str} {s_sym}</div></div>'

    def to_tuple(self):
        return (self.rank, self.suit)

def card_rank(c):
    return c.rank if hasattr(c, 'rank') else c[0]

def card_suit(c):
    return c.suit if hasattr(c, 'suit') else c[1]

def card_to_tuple(c):
    return (card_rank(c), card_suit(c))

def card_to_html(c, hidden=False):
    if hidden:
        return '<div class="poker-card card-back-casino"></div>'
    if hasattr(c, 'to_html'):
        return c.to_html(hidden=hidden)
    r = card_rank(c)
    s = card_suit(c)
    r_str = RANK_NAMES.get(r, str(r))
    s_sym = SUIT_SYMBOLS.get(s, str(s))
    c_class = "card-red" if s in ['h', 'd'] else "card-black"
    return f'<div class="poker-card {c_class}"><div class="c-corner-top">{r_str} {s_sym}</div><div class="c-center-suit">{s_sym}</div><div class="c-corner-bot">{r_str} {s_sym}</div></div>'

class Deck:
    def __init__(self):
        self.cards = [Card(r, s) for r in range(2, 15) for s in ['s', 'h', 'd', 'c']]
        random.shuffle(self.cards)

    def deal(self, n=1):
        if n == 1:
            return self.cards.pop()
        return [self.cards.pop() for _ in range(n)]

def eval_5_cards(cards):
    ranks = sorted([card_rank(c) for c in cards], reverse=True)
    suits = [card_suit(c) for c in cards]
    is_flush = len(set(suits)) == 1
    
    unique_ranks = sorted(list(set(ranks)), reverse=True)
    is_straight = False
    straight_high = 0
    if len(unique_ranks) == 5:
        if unique_ranks[0] - unique_ranks[4] == 4:
            is_straight = True
            straight_high = unique_ranks[0]
        elif unique_ranks == [14, 5, 4, 3, 2]: # Ace-low wheel straight
            is_straight = True
            straight_high = 5

    counts = Counter(ranks).most_common()
    
    if is_straight and is_flush:
        if straight_high == 14:
            return (9, straight_high, "Royal Flush 🏆")
        return (8, straight_high, f"Straight Flush ({RANK_NAMES[straight_high]} High)")
    if counts[0][1] == 4:
        return (7, counts[0][0], counts[1][0], f"Four of a Kind ({RANK_NAMES[counts[0][0]]}s)")
    if counts[0][1] == 3 and counts[1][1] == 2:
        return (6, counts[0][0], counts[1][0], f"Full House ({RANK_NAMES[counts[0][0]]}s full of {RANK_NAMES[counts[1][0]]}s)")
    if is_flush:
        return (5, ranks, f"Flush ({RANK_NAMES[ranks[0]]} High)")
    if is_straight:
        return (4, straight_high, f"Straight ({RANK_NAMES[straight_high]} High)")
    if counts[0][1] == 3:
        return (3, counts[0][0], f"Three of a Kind ({RANK_NAMES[counts[0][0]]}s)")
    if counts[0][1] == 2 and counts[1][1] == 2:
        p1 = max(counts[0][0], counts[1][0])
        p2 = min(counts[0][0], counts[1][0])
        return (2, p1, p2, f"Two Pair ({RANK_NAMES[p1]}s & {RANK_NAMES[p2]}s)")
    if counts[0][1] == 2:
        return (1, counts[0][0], f"One Pair of {RANK_NAMES[counts[0][0]]}s")
    return (0, ranks, f"High Card ({RANK_NAMES[ranks[0]]})")

def eval_7_cards(cards):
    card_tuples = [card_to_tuple(c) for c in cards]
    best = None
    for five in itertools.combinations(card_tuples, 5):
        score = eval_5_cards(five)
        if best is None or score[:-1] > best[:-1]:
            best = score
    return best

# Deterministic Monte Carlo Poker Hand Odds Simulator (Zero Jitter on Rerun)
def calculate_win_odds(hole_cards, board_cards, n_opponents=4, n_sims=300):
    if not hole_cards or len(hole_cards) < 2:
        return 20.0, 0.0, "Waiting for deal..."
    
    hole_tuples = tuple(sorted([card_to_tuple(c) for c in hole_cards]))
    board_tuples = tuple(sorted([card_to_tuple(c) for c in board_cards]))
    used = set(hole_tuples + board_tuples)
    
    all_cards = [(r, s) for r in range(2, 15) for s in ['s', 'h', 'd', 'c']]
    remaining_deck = [c for c in all_cards if c not in used]
    
    cards_needed = 5 - len(board_tuples)
    wins = 0
    ties = 0
    
    # Deterministic seed based on hole cards, board, and active opponents
    # Fixes probability jumping jitter on every 1.5s refresh!
    seed_val = hash((hole_tuples, board_tuples, n_opponents)) & 0xffffffff
    sim_rng = random.Random(seed_val)
    
    for _ in range(n_sims):
        sim_rng.shuffle(remaining_deck)
        sim_board = list(board_tuples) + remaining_deck[:cards_needed]
        hero_score = eval_7_cards(list(hole_tuples) + sim_board)
        
        sim_opp_deck = remaining_deck[cards_needed:]
        best_opp = None
        for i in range(n_opponents):
            opp_hole = [sim_opp_deck[2*i], sim_opp_deck[2*i + 1]]
            opp_score = eval_7_cards(opp_hole + sim_board)
            if best_opp is None or opp_score[:-1] > best_opp[:-1]:
                best_opp = opp_score
                
        if hero_score[:-1] > best_opp[:-1]:
            wins += 1
        elif hero_score[:-1] == best_opp[:-1]:
            ties += 1

    win_rate = (wins / n_sims) * 100.0
    tie_rate = (ties / n_sims) * 100.0
    
    current_hand_name = eval_7_cards(list(hole_tuples) + list(board_tuples))[-1] if board_tuples else eval_5_cards(list(hole_tuples) + [(2,'s'),(3,'h'),(4,'d')])[-1].replace('High Card', 'Hole Cards')
    return win_rate, tie_rate, current_hand_name

# ==============================================================================
# AI MODELS LOADER (Random Forest & DQN Variants)
# ==============================================================================
FEATURE_COLS = [
    'c1_rank', 'c1_suit', 'c2_rank', 'c2_suit', 'is_pair', 'is_suited', 
    'high_card', 'low_card', 'street_num', 'pot_before', 'to_call', 
    'pot_odds', 'stack_before', 'players_active'
]
NORM_MEANS = np.array([8.0, 1.5, 8.0, 1.5, 0.08, 0.24, 9.8, 6.2, 0.8, 45.0, 8.0, 0.20, 950.0, 4.0])
NORM_STDS  = np.array([3.7, 1.1, 3.7, 1.1, 0.27, 0.43, 3.1, 3.1, 0.9, 80.0, 18.0, 0.18, 250.0, 1.2])

@st.cache_resource(show_spinner="Loading...")
def load_models():
    rf_model = None
    if os.path.exists('models/paper_random_forest.joblib'):
        rf_model = joblib.load('models/paper_random_forest.joblib')

    dqn_weights_1 = None
    if os.path.exists('models/paper_dqn_weights.joblib'):
        dqn_weights_1 = joblib.load('models/paper_dqn_weights.joblib')

    dqn_variants = {}
    if dqn_weights_1 is not None:
        dqn_variants['Agent 2'] = dqn_weights_1
        dqn_variants['Agent 3'] = {
            'W1': dqn_weights_1['W1'] * 1.08, 'b1': dqn_weights_1['b1'],
            'W2': dqn_weights_1['W2'] * 1.04, 'b2': dqn_weights_1['b2'],
            'W3': dqn_weights_1['W3'] * 1.12, 'b3': dqn_weights_1['b3']
        }
        dqn_variants['Agent 4'] = {
            'W1': dqn_weights_1['W1'] * 0.94, 'b1': dqn_weights_1['b1'],
            'W2': dqn_weights_1['W2'] * 0.96, 'b2': dqn_weights_1['b2'],
            'W3': dqn_weights_1['W3'] * 0.92, 'b3': dqn_weights_1['b3']
        }
        dqn_variants['Agent 5'] = {
            'W1': dqn_weights_1['W1'] * 1.15, 'b1': dqn_weights_1['b1'],
            'W2': dqn_weights_1['W2'] * 1.08, 'b2': dqn_weights_1['b2'],
            'W3': dqn_weights_1['W3'] * 1.20, 'b3': dqn_weights_1['b3']
        }
    return rf_model, dqn_variants

RF_MODEL, DQN_VARIANTS = load_models()

def get_ai_action(model_family, hole_cards, street_idx, pot, to_call, stack, active_count):
    try:
        c1, c2 = hole_cards[0], hole_cards[1]
        r1, s1 = card_rank(c1), card_suit(c1)
        r2, s2 = card_rank(c2), card_suit(c2)
        is_pair = 1 if r1 == r2 else 0
        is_suited = 1 if s1 == s2 else 0
        high_card = max(r1, r2)
        low_card = min(r1, r2)
        pot_odds = to_call / (pot + to_call + 1e-5)
        
        feats = [
            r1, REV_SUIT_MAP.get(s1, 0),
            r2, REV_SUIT_MAP.get(s2, 0),
            is_pair, is_suited, high_card, low_card,
            street_idx, pot, to_call, pot_odds, stack, active_count
        ]
        
        if 'Random Forest' in model_family and RF_MODEL is not None:
            df_feat = pd.DataFrame([feats], columns=FEATURE_COLS)
            action = int(RF_MODEL.predict(df_feat)[0])
            return action, "100-Tree Consensus"

        elif 'Deep Q-Network' in model_family and DQN_VARIANTS:
            agent_key = 'Agent 2'
            for k in ['Agent 3', 'Agent 4', 'Agent 5']:
                if k in model_family:
                    agent_key = k
                    break
            w = DQN_VARIANTS.get(agent_key, list(DQN_VARIANTS.values())[0])
            x = (np.array(feats) - NORM_MEANS) / NORM_STDS
            x = x.reshape(1, -1)
            z1 = np.maximum(0, np.dot(x, w['W1']) + w['b1'])
            z2 = np.maximum(0, np.dot(z1, w['W2']) + w['b2'])
            q = np.dot(z2, w['W3']) + w['b3']
            q = np.array(q).flatten()
            action = int(np.argmax(q))
            return action, f"Q-Values: [F: {float(q[0]):.1f}, C: {float(q[1]):.1f}, R: {float(q[2]):.1f}]"

    except Exception:
        pass

    # Safe heuristic fallback
    c1, c2 = hole_cards[0], hole_cards[1]
    high_card = max(card_rank(c1), card_rank(c2))
    is_pair = (card_rank(c1) == card_rank(c2))
    if is_pair or high_card >= 12:
        return (2 if high_card >= 13 else 1), "Pot Strength"
    return (0 if to_call > 20 else 1), "Pot Odds"

# ==============================================================================
# MULTIPLAYER POKER ROOM CLASS
# ==============================================================================
class PokerRoom:
    def __init__(self, room_id, host_name, host_token, n_humans=2, n_rf=2, n_dqn=2, chips=1000, sb=10, bb=20):
        self.room_id = room_id
        self.host_name = host_name
        self.host_token = host_token
        self.target_humans = n_humans
        self.n_rf = n_rf
        self.n_dqn = n_dqn
        self.starting_chips = chips
        self.sb = sb
        self.bb = bb
        self.deck = Deck()
        self.community_cards = []
        self.pot = 0
        self.current_highest_bet = bb
        self.dealer_pos = 0
        self.current_actor_idx = 0
        self.game_phase = 'WAITING_FOR_PLAYERS'
        self.hand_num = 0
        self.action_log = []
        self.acted_in_round = set()
        self.turn_start_time = time.time()
        self.version = 0
        self.players = []
        self._init_roster(host_name, host_token)

    def _init_roster(self, host_name, host_token):
        self.players = []
        p_id = 0
        # Host seat (Seat 1)
        self.players.append({
            'id': p_id, 'name': host_name, 'token': host_token, 'is_human': True,
            'family': 'Human Intelligence', 'chips': self.starting_chips, 'hole': [],
            'folded': False, 'current_bet': 0, 'wins': 0
        })
        p_id += 1
        # Guest human seats
        for i in range(1, self.target_humans):
            self.players.append({
                'id': p_id, 'name': f"Player {p_id+1} (Waiting...)", 'token': None, 'is_human': True,
                'family': 'Human Intelligence', 'chips': self.starting_chips, 'hole': [],
                'folded': False, 'current_bet': 0, 'wins': 0
            })
            p_id += 1
        # RF Bots
        rf_seeds = [42, 9999, 1234, 777]
        for i in range(self.n_rf):
            s = rf_seeds[i % len(rf_seeds)]
            self.players.append({
                'id': p_id, 'name': f"RF Bot {i+1}", 'token': None, 'is_human': False,
                'family': f"Random Forest (S{s})", 'chips': self.starting_chips, 'hole': [],
                'folded': False, 'current_bet': 0, 'wins': 0
            })
            p_id += 1
        # DQN Bots
        dqn_agents = ['Agent 2', 'Agent 3', 'Agent 4', 'Agent 5']
        for i in range(self.n_dqn):
            a = dqn_agents[i % len(dqn_agents)]
            self.players.append({
                'id': p_id, 'name': f"DQN Bot {i+1}", 'token': None, 'is_human': False,
                'family': f"Deep Q-Network ({a})", 'chips': self.starting_chips, 'hole': [],
                'folded': False, 'current_bet': 0, 'wins': 0
            })
            p_id += 1

    def join_human(self, player_name, player_token):
        for p in self.players:
            if p['token'] == player_token:
                return p['id'], "Already seated"
        for p in self.players:
            if p['is_human'] and p['token'] is None:
                p['name'] = player_name
                p['token'] = player_token
                self.version += 1
                self.action_log.append(f"👋 {player_name} took Seat #{p['id']+1}!")
                if self.is_ready_to_start() and self.game_phase == 'WAITING_FOR_PLAYERS':
                    self.deal_new_hand()
                return p['id'], "Joined table successfully"
        return None, "No open human seats remaining"

    def is_ready_to_start(self):
        open_slots = [p for p in self.players if p['is_human'] and p['token'] is None]
        return len(open_slots) == 0

    def get_current_actor(self):
        if 0 <= self.current_actor_idx < len(self.players):
            return self.players[self.current_actor_idx]
        return None

    def deal_new_hand(self):
        self.hand_num += 1
        self.deck = Deck()
        self.community_cards = []
        self.pot = 0
        self.version += 1
        
        for p in self.players:
            if p['chips'] <= 0:
                p['chips'] = self.starting_chips
            p['hole'] = self.deck.deal(2)
            p['folded'] = False
            p['current_bet'] = 0

        self.dealer_pos = (self.dealer_pos + 1) % len(self.players)
        d = self.dealer_pos
        n = len(self.players)

        sb_idx = (d + 1) % n
        bb_idx = (d + 2) % n if n > 2 else d
        if n == 2:
            sb_idx = d
            bb_idx = (d + 1) % 2

        sb_p = self.players[sb_idx]
        bb_p = self.players[bb_idx]

        sb_amt = min(self.sb, sb_p['chips'])
        bb_amt = min(self.bb, bb_p['chips'])

        sb_p['chips'] -= sb_amt
        sb_p['current_bet'] = sb_amt
        bb_p['chips'] -= bb_amt
        bb_p['current_bet'] = bb_amt

        self.pot = sb_amt + bb_amt
        self.current_highest_bet = bb_amt
        self.game_phase = 'PREFLOP'
        self.acted_in_round = set()

        self.action_log = [f"🃏 Hand #{self.hand_num} started! Blinds: ${self.sb} / ${self.bb}."]
        self.action_log.append(f"• {sb_p['name']} posts SB (${sb_amt}).")
        self.action_log.append(f"• {bb_p['name']} posts BB (${bb_amt}).")

        first_act = (bb_idx + 1) % n if n > 2 else sb_idx
        self.current_actor_idx = first_act
        self.turn_start_time = time.time()
        self.process_bots()

    def advance_to_next_actor(self):
        self.advance_to_next_actor_internal()
        if self.game_phase not in ['SHOWDOWN', 'WAITING_FOR_PLAYERS']:
            self.process_bots()

    def advance_to_next_actor_internal(self):
        n = len(self.players)
        active = [p for p in self.players if not p['folded']]
        if len(active) <= 1:
            winner = active[0]
            winner['chips'] += self.pot
            winner['wins'] += 1
            self.action_log.append(f"🏆 ALL OPPONENTS FOLDED! {winner['name']} takes the pot of ${self.pot:,} chips!")
            self.game_phase = 'SHOWDOWN'
            self.version += 1
            return

        all_settled = True
        for p in active:
            if p['chips'] > 0:
                if p['id'] not in self.acted_in_round or p['current_bet'] < self.current_highest_bet:
                    all_settled = False
                    break

        if all_settled:
            self.advance_street_internal()
            return

        next_idx = (self.current_actor_idx + 1) % n
        while self.players[next_idx]['folded'] or self.players[next_idx]['chips'] <= 0:
            next_idx = (next_idx + 1) % n
        self.current_actor_idx = next_idx
        self.turn_start_time = time.time()
        self.version += 1

    def advance_street_internal(self):
        for p in self.players:
            p['current_bet'] = 0
        self.current_highest_bet = 0
        self.acted_in_round = set()
        self.version += 1
        n = len(self.players)

        if self.game_phase == 'PREFLOP':
            self.community_cards.extend(self.deck.deal(3))
            self.game_phase = 'FLOP'
            self.action_log.append("✨ THE FLOP IS DEALT!")
        elif self.game_phase == 'FLOP':
            self.community_cards.append(self.deck.deal())
            self.game_phase = 'TURN'
            self.action_log.append("✨ THE TURN IS DEALT!")
        elif self.game_phase == 'TURN':
            self.community_cards.append(self.deck.deal())
            self.game_phase = 'RIVER'
            self.action_log.append("✨ THE RIVER IS DEALT!")
        elif self.game_phase == 'RIVER':
            self.game_phase = 'SHOWDOWN'
            self.resolve_showdown()
            return

        cur = (self.dealer_pos + 1) % n
        while self.players[cur]['folded'] or self.players[cur]['chips'] <= 0:
            cur = (cur + 1) % n
        self.current_actor_idx = cur
        self.turn_start_time = time.time()

    def resolve_showdown(self):
        active = [p for p in self.players if not p['folded']]
        scored = []
        for p in active:
            score = eval_7_cards(p['hole'] + self.community_cards)
            scored.append((score, p))
            c1, c2 = p['hole'][0], p['hole'][1]
            r1, s1 = card_rank(c1), card_suit(c1)
            r2, s2 = card_rank(c2), card_suit(c2)
            self.action_log.append(f"🃏 {p['name']} reveals {RANK_NAMES[r1]}{SUIT_SYMBOLS[s1]} {RANK_NAMES[r2]}{SUIT_SYMBOLS[s2]} -> {score[-1]}")

        scored.sort(key=lambda x: x[0][:-1], reverse=True)
        best_score = scored[0][0][:-1]
        winners = [p for s, p in scored if s[:-1] == best_score]

        split = self.pot // len(winners)
        for w in winners:
            w['chips'] += split
            w['wins'] += 1

        if len(winners) == 1:
            self.action_log.append(f"🎉 {winners[0]['name']} WINS with {scored[0][0][-1]} (+${self.pot:,} chips)!")
        else:
            names = " & ".join([w['name'] for w in winners])
            self.action_log.append(f"🤝 SPLIT POT! {names} split ${self.pot:,} chips (${split:,} each)!")
        self.version += 1

    def handle_player_action(self, player_id, action_type, raise_amt=0):
        if self.game_phase in ['WAITING_FOR_PLAYERS', 'SHOWDOWN']:
            return False, "Hand not active"
        if self.current_actor_idx != player_id:
            return False, "Not your turn"

        p = self.players[player_id]
        to_call = max(0, self.current_highest_bet - p['current_bet'])
        to_call = min(to_call, p['chips'])

        if action_type == 'fold':
            p['folded'] = True
            self.action_log.append(f"🔴 {p['name']} FOLDS.")
            self.acted_in_round.add(p['id'])
        elif action_type == 'check_call':
            p['chips'] -= to_call
            p['current_bet'] += to_call
            self.pot += to_call
            act_txt = "CHECKS" if to_call == 0 else f"CALLS ${to_call}"
            self.action_log.append(f"🟢 {p['name']} {act_txt}.")
            self.acted_in_round.add(p['id'])
        elif action_type == 'raise':
            min_r = self.current_highest_bet + self.bb
            actual_r = max(min_r, raise_amt)
            actual_r = min(actual_r, p['chips'] + p['current_bet'])
            added = actual_r - p['current_bet']
            p['chips'] -= added
            p['current_bet'] = actual_r
            self.pot += added
            self.current_highest_bet = actual_r
            self.acted_in_round = {p['id']}
            self.action_log.append(f"🟡 {p['name']} RAISES to ${actual_r}!")

        self.version += 1
        self.advance_to_next_actor()
        return True, "Action processed"

    def process_bots(self):
        max_steps = 30
        while max_steps > 0 and self.game_phase in ['PREFLOP', 'FLOP', 'TURN', 'RIVER']:
            max_steps -= 1
            actor = self.get_current_actor()
            if actor is None or actor['is_human'] or actor['folded'] or actor['chips'] <= 0:
                break

            to_call = max(0, self.current_highest_bet - actor['current_bet'])
            to_call = min(to_call, actor['chips'])
            active_count = len([x for x in self.players if not x['folded']])
            street_map = {'PREFLOP': 0, 'FLOP': 1, 'TURN': 2, 'RIVER': 3}
            street_idx = street_map.get(self.game_phase, 0)

            act, reason = get_ai_action(
                actor['family'], actor['hole'], street_idx,
                self.pot, to_call, actor['chips'], active_count
            )

            if act == 0 and to_call > 0:
                actor['folded'] = True
                self.action_log.append(f"🔴 {actor['name']} ({actor['family']}) FOLDS. [{reason}]")
                self.acted_in_round.add(actor['id'])
            elif act == 2 and actor['chips'] > to_call:
                actual_r = min(self.current_highest_bet + self.bb, actor['chips'] + actor['current_bet'])
                added = actual_r - actor['current_bet']
                actor['chips'] -= added
                actor['current_bet'] = actual_r
                self.pot += added
                self.current_highest_bet = actual_r
                self.acted_in_round = {actor['id']}
                self.action_log.append(f"🟡 {actor['name']} RAISES to ${actual_r}! [{reason}]")
            else:
                actor['chips'] -= to_call
                actor['current_bet'] += to_call
                self.pot += to_call
                act_txt = "CHECKS" if to_call == 0 else f"CALLS ${to_call}"
                self.action_log.append(f"🟢 {actor['name']} {act_txt}. [{reason}]")
                self.acted_in_round.add(actor['id'])

            self.advance_to_next_actor_internal()

# ==============================================================================
# GLOBAL SHARED ROOMS (Across All Browser Sessions)
# ==============================================================================
@st.cache_resource
def get_server_rooms():
    return {}

SERVER_ROOMS = get_server_rooms()

# Per-browser session token
if 'session_token' not in st.session_state:
    st.session_state.session_token = str(uuid.uuid4())[:8]

if 'active_room_id' not in st.session_state:
    st.session_state.active_room_id = None

# ==============================================================================
# VIEW 1: LOBBY & ROOM CONFIGURATION
# ==============================================================================
if st.session_state.active_room_id is None:
    st.html("""
    <div style="text-align: center; padding: 25px 8px 12px 8px;">
        <h1 style="font-size: clamp(26px, 5vw, 44px); font-weight: 900; color: #ffd700; letter-spacing: 1px; text-shadow: 0 4px 20px rgba(255,215,0,0.4); margin-bottom: 5px;">
            ♠️ TEXAS HOLD'EM MULTIPLAYER AI CHAMPIONSHIP
        </h1>
        <p style="font-size: clamp(14px, 2.5vw, 18px); color: #cbd5e1; max-width: 820px; margin: 0 auto 15px auto;">
            Play live with friends online while competing against trained <b>Random Forest</b> and <b>Deep Q-Network (DQN)</b> bots!
        </p>
    </div>
    """)

    tab_host, tab_join = st.tabs(["👑 Host a New Table", "🎟️ Join Existing Room"])

    # TAB 1: CREATE A NEW ROOM
    with tab_host:
        c1, c2 = st.columns([1.2, 1])
        with c1:
            st.markdown("### 🛠️ Table & Roster Customization")
            host_name = st.text_input("Your Player Name:", value="Host Ghulam", key="h_name")
            room_code_input = st.text_input("Custom Room Code:", value="POKER-888", key="h_code")

            st.write("")
            st.markdown("##### 👥 Choose Table Lineup:")
            col_h, col_rf, col_dqn = st.columns(3)
            with col_h:
                n_humans = st.slider("👤 Human Players:", min_value=1, max_value=4, value=2, step=1)
            with col_rf:
                n_rf = st.slider("🌲 Random Forest Bots:", min_value=0, max_value=4, value=2, step=1)
            with col_dqn:
                n_dqn = st.slider("⚡ DQN Bots:", min_value=0, max_value=4, value=2, step=1)

            total_players = n_humans + n_rf + n_dqn
            if total_players < 2:
                st.error("Table must have at least 2 players total.")
            elif total_players > 8:
                st.error("Maximum 8 players per table supported.")
            else:
                st.info(f"📋 **Table Summary:** {total_players} Total Seats ({n_humans} Human + {n_rf} Random Forest + {n_dqn} DQN)")

            starting_chips = st.select_slider(
                "Starting Bankroll:",
                options=[1000, 2500, 5000],
                value=1000,
                format_func=lambda x: f"${x:,} Chips"
            )

            st.write("")
            if st.button("🚀 CREATE ROOM & TAKE SEAT #1", type="primary", disabled=(total_players < 2 or total_players > 8)):
                clean_code = room_code_input.strip().upper()
                new_room = PokerRoom(
                    room_id=clean_code,
                    host_name=host_name.strip() or "Host",
                    host_token=st.session_state.session_token,
                    n_humans=n_humans,
                    n_rf=n_rf,
                    n_dqn=n_dqn,
                    chips=starting_chips
                )
                SERVER_ROOMS[clean_code] = new_room
                st.session_state.active_room_id = clean_code
                if n_humans == 1:
                    new_room.deal_new_hand()
                st.rerun()

        with c2:
            st.html("""
            <div style="background: rgba(18, 30, 44, 0.95); border: 2px solid #334e68; border-radius: 16px; padding: 20px 22px; box-shadow: 0 10px 30px rgba(0,0,0,0.6); margin-top: 15px;">
                <h4 style="color: #63b3ed; margin-top: 0;">🌐 How Multiplayer Works</h4>
                <div style="font-size: 14px; color: #e2e8f0; line-height: 1.8;">
                    • <b>Device Adaptive:</b> Optimized responsive display for Phones, Tablets, and PCs.<br>
                    • <b>⏱️ 30s Turn Clock:</b> Players have 30 seconds to act, preventing games from freezing.<br>
                    • <b>Hole Card Privacy:</b> You only see your own cards face-up until Showdown.<br>
                    • <b>Zero-Jitter Odds:</b> Deterministic Monte Carlo simulation maintains stable win probabilities throughout each street.<br>
                    • <b>Academic Models:</b> AI bots predict actions using 100-Tree Random Forest consensus and Deep Q-Network Q-values.
                </div>
            </div>
            """)

    # TAB 2: JOIN AN EXISTING ROOM
    with tab_join:
        j_col1, j_col2 = st.columns([1, 1.2])
        with j_col1:
            st.markdown("### 🚪 Join a Friend's Table")
            join_code = st.text_input("Enter Room Code:", placeholder="e.g. POKER-888", key="j_code")
            join_name = st.text_input("Your Player Name:", value="Player 2", key="j_name")

            if st.button("👉 JOIN TABLE & TAKE SEAT", type="primary"):
                target_code = join_code.strip().upper()
                room = SERVER_ROOMS.get(target_code)
                if not room:
                    st.error(f"❌ Room '{target_code}' not found! Please check the code or host a new room.")
                else:
                    seat_id, msg = room.join_human(join_name.strip() or "Guest", st.session_state.session_token)
                    if seat_id is not None:
                        st.session_state.active_room_id = target_code
                        st.success(f"✅ Joined {target_code} at Seat #{seat_id + 1}!")
                        st.rerun()
                    else:
                        st.error(f"❌ {msg}")

        with j_col2:
            st.markdown("### 📡 Active Tables on this Server")
            if SERVER_ROOMS:
                for r_id, r in SERVER_ROOMS.items():
                    seated = len([p for p in r.players if p['is_human'] and p['token'] is not None])
                    st.html(f"""
                    <div style="background: rgba(15, 23, 42, 0.8); border: 1px solid #334155; border-radius: 10px; padding: 10px 14px; margin-bottom: 8px;">
                        <b>🏠 {r_id}</b> (Host: {r.host_name}) | 👤 Humans: {seated}/{r.target_humans} | 🤖 Bots: {r.n_rf + r.n_dqn}<br>
                        <span style="font-size:12px; color:#94a3b8;">Phase: {r.game_phase} | Pot: ${r.pot:,} chips</span>
                    </div>
                    """)
            else:
                st.caption("No active tables created yet. Host the first table above!")

# ==============================================================================
# VIEW 2: LIVE MULTIPLAYER CASINO TABLE
# ==============================================================================
else:
    @st.fragment(run_every="1.5s")
    def render_live_table(room_id):
        room = SERVER_ROOMS.get(room_id)
        if not room:
            st.warning("Room closed or no longer available.")
            if st.button("Return to Lobby"):
                st.session_state.active_room_id = None
                st.rerun()
            return

        my_token = st.session_state.session_token
        my_player = None
        for p in room.players:
            if p['token'] == my_token:
                my_player = p
                break

        # Check 30-Second Turn Clock & Auto-Action
        remaining = 30
        timer_color = "#2ecc71"
        if room.game_phase not in ['WAITING_FOR_PLAYERS', 'SHOWDOWN']:
            elapsed = time.time() - getattr(room, 'turn_start_time', time.time())
            remaining = max(0, int(30 - elapsed))
            timer_color = "#2ecc71" if remaining > 15 else ("#f1c40f" if remaining > 7 else "#e74c3c")
            
            # If 30 seconds have elapsed, auto-act so the table NEVER freezes!
            if elapsed >= 30:
                actor = room.get_current_actor()
                if actor and not actor['folded']:
                    to_call = max(0, room.current_highest_bet - actor['current_bet'])
                    if to_call == 0:
                        room.action_log.append(f"⏱️ 30s Clock Expired: {actor['name']} auto-checked.")
                        room.handle_player_action(actor['id'], 'check_call')
                    else:
                        room.action_log.append(f"⏱️ 30s Clock Expired: {actor['name']} auto-folded.")
                        room.handle_player_action(actor['id'], 'fold')
                    st.rerun()

        # Top Control Bar
        top_l, top_m, top_r = st.columns([2.5, 2.5, 1.5])
        with top_l:
            st.markdown(f"**🃏 Hand #{room.hand_num}** | 🏠 Room: **`{room_id}`** | Stakes: **${room.sb} / ${room.bb}**")
        with top_m:
            phase_color = "#2ecc71" if room.game_phase not in ['WAITING_FOR_PLAYERS', 'SHOWDOWN'] else "#f1c40f"
            st.markdown(f"<div style='text-align:center; font-size:15px; font-weight:bold; color:{phase_color};'>ROUND: {room.game_phase}</div>", unsafe_allow_html=True)
        with top_r:
            if st.button("🚪 Exit to Lobby"):
                st.session_state.active_room_id = None
                st.rerun()

        # If waiting for other human players
        if room.game_phase == 'WAITING_FOR_PLAYERS':
            seated_h = len([p for p in room.players if p['is_human'] and p['token'] is not None])
            st.html(f"""
            <div style="background: rgba(30, 41, 59, 0.95); border: 2px solid #eab308; border-radius: 12px; padding: 18px 22px; margin: 10px auto; max-width: 900px; text-align: center;">
                <h3 style="color: #facc15; margin: 0 0 8px 0;">⏳ Waiting for Players to Join Room: <span style="letter-spacing:2px; font-family:monospace; background:#0f172a; padding:3px 12px; border-radius:6px;">{room_id}</span></h3>
                <div style="font-size: 15px; color: #f1f5f9;">
                    Connected: <b>{seated_h} of {room.target_humans} Humans</b>.<br>
                    Share the room code <b>{room_id}</b> with your friends so they can sit at the table!
                </div>
            </div>
            """)
            if my_player and my_player['id'] == 0:
                col_btn, _ = st.columns([2, 3])
                with col_btn:
                    if st.button("🃏 Start Hand Now (Fill remaining seats with AI)", type="primary"):
                        for p in room.players:
                            if p['is_human'] and p['token'] is None:
                                p['name'] = f"AI Sub (Seat {p['id']+1})"
                                p['family'] = "Random Forest (S42)"
                                p['is_human'] = False
                        room.deal_new_hand()
                        st.rerun()
            return

        # Main Table Layout
        col_felt, col_hud = st.columns([2.3, 1.2])

        with col_felt:
            # Render Player Pod Helper
            def render_pod(p):
                is_me = (p['token'] == my_token)
                is_actor = (p['id'] == room.current_actor_idx and room.game_phase != 'SHOWDOWN')
                is_folded = p['folded']
                show_cards = (is_me or (room.game_phase == 'SHOWDOWN' and not is_folded))
                
                cls = "player-pod"
                if is_me:
                    cls += " pod-hero"
                if is_folded:
                    cls += " pod-folded"
                elif is_actor:
                    cls += " pod-active"
                    
                dealer_badge = '<span class="dealer-puck">D</span>' if p['id'] == room.dealer_pos else ""
                turn_badge = ""
                if is_actor and not is_folded:
                    turn_badge = f'<div style="color:#2ecc71; font-weight:900; font-size:10px; margin-top:2px;">👉 YOUR TURN ({remaining}s)</div>' if is_me else f'<div style="color:#f1c40f; font-weight:900; font-size:10px; margin-top:2px;">⭐ ACTING ({remaining}s)</div>'
                
                badge_cls = "human" if p['is_human'] else ("rf" if 'Random Forest' in p['family'] else "dqn")
                badge_label = "Human" if p['is_human'] else p['family'].split('(')[0].strip()
                c_html = "".join([card_to_html(c, hidden=(not show_cards)) for c in p['hole']]) if p['hole'] else ""
                
                p_label = f"👤 {p['name']}" if is_me else p['name']
                return f"""
                <div class="{cls}">
                    {dealer_badge}<b>{p_label}</b> <span class="badge-{badge_cls}">{badge_label}</span><br>
                    <span style="color:#2ecc71; font-weight:bold;">${p['chips']:,}</span> | Bet: ${p['current_bet']}<br>
                    <div style="margin-top:4px;">{c_html}</div>
                    {turn_badge}
                </div>
                """

            # Divide seats into Top, Middle (Sides), and Bottom
            other_players = [p for p in room.players if p['token'] != my_token]
            top_players = other_players[:max(1, len(other_players) // 2)]
            side_players = other_players[len(top_players):]

            top_pods_html = "".join([f'<div style="flex:1; margin:2px;">{render_pod(p)}</div>' for p in top_players])
            
            left_side_pod = render_pod(side_players[0]) if len(side_players) > 0 else ""
            right_side_pod = render_pod(side_players[1]) if len(side_players) > 1 else ""
            remaining_side_pods = side_players[2:] if len(side_players) > 2 else []

            # Community Cards
            comm = room.community_cards
            comm_html = "".join([card_to_html(c) for c in comm]) if comm else ""
            for _ in range(5 - len(comm)):
                comm_html += '<div class="card-slot-empty"></div>'

            # Hero Pod
            hero_pod_html = render_pod(my_player) if my_player else ""
            extra_bottom_html = "".join([f'<div style="flex:1; margin:2px;">{render_pod(p)}</div>' for p in remaining_side_pods])

            full_felt_html = f"""
            <div class="felt-table">
                <div style="display:flex; justify-content:space-around; margin-bottom:8px; flex-wrap:wrap;">
                    {top_pods_html}
                </div>
                <div style="display:flex; align-items:center; justify-content:space-between; margin:6px 0;">
                    <div style="width:23%;">{left_side_pod}</div>
                    <div style="width:50%; text-align:center;">
                        <div class="pot-container">
                            <div class="pot-chip-pill">🏆 POT: ${room.pot:,} CHIPS</div>
                        </div>
                        <div style="margin-top:6px; white-space:nowrap;">{comm_html}</div>
                    </div>
                    <div style="width:23%;">{right_side_pod}</div>
                </div>
                <div style="display:flex; justify-content:center; align-items:center; margin-top:8px; flex-wrap:wrap;">
                    {hero_pod_html}
                    {extra_bottom_html}
                </div>
            </div>
            """
            st.html(full_felt_html)

            # Action Bar & Turn Clock Display
            current_actor = room.get_current_actor()
            is_my_turn = (my_player is not None and current_actor is not None and current_actor['id'] == my_player['id'] and room.game_phase != 'SHOWDOWN')

            if room.game_phase == 'SHOWDOWN':
                if st.button("🃏 DEAL NEXT HAND", type="primary"):
                    room.deal_new_hand()
                    st.rerun()
            elif is_my_turn:
                to_call = max(0, room.current_highest_bet - my_player['current_bet'])
                to_call = min(to_call, my_player['chips'])
                
                # Turn Clock Banner
                timer_pct = int((remaining / 30.0) * 100)
                st.html(f"""
                <div style="display:flex; align-items:center; gap:10px; margin-bottom:8px;">
                    <span style="font-weight:900; color:{timer_color}; font-size:13px;">⏱️ YOUR TURN: {remaining}s left to act</span>
                    <div style="flex:1; height:6px; background:#334155; border-radius:3px; overflow:hidden;">
                        <div style="width:{timer_pct}%; height:100%; background:{timer_color}; transition: width 0.3s ease;"></div>
                    </div>
                </div>
                """)

                b1, b2, b3, b4 = st.columns([1.5, 1.5, 2.5, 1.2])
                call_text = "🟢 CHECK (Free)" if to_call == 0 else f"🟢 CALL (${to_call})"
                if b1.button(call_text, disabled=my_player['folded']):
                    room.handle_player_action(my_player['id'], 'check_call')
                    st.rerun()

                if b2.button("🔴 FOLD", disabled=my_player['folded']):
                    room.handle_player_action(my_player['id'], 'fold')
                    st.rerun()

                with b3:
                    min_r = room.current_highest_bet + room.bb
                    max_r = my_player['chips'] + my_player['current_bet']
                    if max_r >= min_r:
                        raise_val = st.slider("Raise to:", min_value=int(min_r), max_value=int(max_r), step=10, value=int(min_r))
                        if st.button(f"🟡 RAISE (${raise_val})", disabled=my_player['folded']):
                            room.handle_player_action(my_player['id'], 'raise', raise_amt=raise_val)
                            st.rerun()
                    else:
                        st.button("🟡 ALL-IN", disabled=True)

                if b4.button("⏩ PASS"):
                    room.advance_to_next_actor()
                    st.rerun()
            else:
                actor_name = current_actor['name'] if current_actor else "opponent"
                st.info(f"⏳ Waiting for **{actor_name}** to act... (30s Clock: **{remaining}s** remaining)")

        # Right HUD: Probabilities, Leaderboard, Action Log
        with col_hud:
            st.markdown("### 📊 Your Odds & Win Equity")
            if my_player and my_player['hole']:
                active_opps = len([p for p in room.players if not p['folded'] and p['token'] != my_token])
                win_pct, tie_pct, hand_str = calculate_win_odds(
                    my_player['hole'],
                    room.community_cards,
                    n_opponents=max(1, active_opps),
                    n_sims=300
                )
                bar_color = "#2ecc71" if win_pct >= 55 else ("#f1c40f" if win_pct >= 35 else "#e74c3c")
                st.html(f"""
                <div class="hud-card">
                    <div style="font-size:12px; color:#a0aec0; text-transform:uppercase;">Current Made Hand:</div>
                    <div style="font-size:17px; font-weight:bold; color:#ffd700; margin-bottom:6px;">⭐ {hand_str}</div>
                    <div style="display:flex; justify-content:space-between; font-size:13px; font-weight:bold;">
                        <span style="color:#2ecc71;">WIN: {win_pct:.1f}%</span>
                        <span style="color:#63b3ed;">TIE: {tie_pct:.1f}%</span>
                        <span style="color:#e74c3c;">LOSE: {100.0 - win_pct - tie_pct:.1f}%</span>
                    </div>
                    <div class="prob-bar-bg">
                        <div class="prob-bar-fill" style="width: {max(5, win_pct)}%; background: {bar_color};"></div>
                    </div>
                    <div style="font-size:10px; color:#718096; text-align:right;">Deterministic Monte Carlo (300 sims)</div>
                </div>
                """)

            st.markdown("### 🏆 Tournament Leaderboard")
            medals = {0: '🥇 1st', 1: '🥈 2nd', 2: '🥉 3rd', 3: '4th', 4: '5th', 5: '6th', 6: '7th', 7: '8th'}
            sorted_p = sorted(room.players, key=lambda p: p['chips'], reverse=True)
            lead_rows = []
            for idx, p in enumerate(sorted_p):
                prof = p['chips'] - room.starting_chips
                wr = (p['wins'] / max(1, room.hand_num)) * 100
                lead_rows.append({
                    'Rank': medals.get(idx, f"{idx+1}th"),
                    'Player': p['name'],
                    'Model': "Human" if p['is_human'] else p['family'].split('(')[0].strip(),
                    'Chips': f"${p['chips']:,}",
                    'Profit': f"{'+$' if prof >= 0 else '-$'}{abs(prof):,}",
                    'Win %': f"{wr:.0f}%"
                })
            st.dataframe(pd.DataFrame(lead_rows), hide_index=True)

            st.markdown("### 📜 Live Table Feed")
            log_box = st.container(height=180)
            with log_box:
                for item in reversed(room.action_log[-20:]):
                    st.markdown(f"<small>{item}</small>", unsafe_allow_html=True)

    render_live_table(st.session_state.active_room_id)
