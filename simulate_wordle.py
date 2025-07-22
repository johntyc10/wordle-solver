import random
import json


def black_chars_check(chars: list, word: str):
    for char in chars:
        if char in word:
            return False
    return True


def yellow_chars_check(yellow_chars: dict, word: str):
    for pos in yellow_chars:
        if word[pos] in yellow_chars[pos]:
            return False
        for char in yellow_chars[pos]:
            if char not in word:
                return False
    return True


def green_chars_check(green_chars: list, word: str):
    for i in range(5):
        if not green_chars[i]:
            continue
        if green_chars[i] != word[i]:
            return False
    return True


def filter_words(black_chars, yellow_chars, green_chars, five_letter_words):
    possible_words = []
    for word in five_letter_words:
        if black_chars_check(black_chars, word) and yellow_chars_check(yellow_chars, word) and green_chars_check(green_chars, word):
            possible_words.append(word)

    return possible_words


def sort_by_reference(reference_list: list, target_list: list):
    """
    Sorts target_list according to the order defined in reference_list.

    Parameters:
    - reference_list: List[str] — Defines the sorting order.
    - target_list: List[str] — Subset of strings to be ordered.

    Returns:
    - A new List[str] with elements of target_list sorted.

    Raises:
    - ValueError: if target_list has elements not present in reference_list.
    """
    target_list_copy = target_list.copy()

    # Build a position lookup for each element in reference_list
    position_map = {value: index for index, value in enumerate(reference_list)}

    # Check for unknown elements
    unknown_items = [item for item in target_list if item not in position_map]
    if unknown_items:
        # print(f"{unknown_items = }")
        for word in unknown_items:
            target_list_copy.remove(word)

    # Sort using the position in reference_list as the key
    return sorted(target_list_copy, key=lambda x: position_map[x]) + unknown_items


def average(list_of_num: list):
    if len(list_of_num) == 0:
        return 0
    return sum(list_of_num) / len(list_of_num)


with open("all_five_letter_words.json", "r") as f:
    persistent_five_letter_words = json.load(f)

with open("five_letter_words_order_by_freq.json", "r") as f:
    five_letter_words_order_by_freq = json.load(f)


used_words = """ABACK ABASE ABATE ABBEY ABIDE ABOUT ABOVE ABYSS ACORN ACRID ACTOR ACUTE ADAGE ADAPT ADEPT ADMIN ADMIT ADOBE ADOPT ADORE ADULT AFFIX AFTER AGAIN AGAPE AGATE AGENT AGILE AGING AGLOW AGONY AGREE AHEAD AISLE ALARM ALBUM ALERT ALIEN ALIKE ALIVE ALLOW ALOFT ALONE ALOOF ALOUD ALPHA ALTAR ALTER AMASS AMBER AMBLE AMISS AMPLE ANGEL ANGER ANGLE ANGRY ANGST ANODE ANTIC ANVIL AORTA APART APHID APPLE APPLY APRON APTLY ARBOR ARDOR ARGUE AROMA ARROW ARTSY ASCOT ASHEN ASIDE ASKEW ASSET ATLAS ATOLL ATONE ATRIA AUDIO AUDIT AVAIL AVERT AWAIT AWAKE AWARD AWARE AWASH AWFUL AXIOM AZURE BACON BADGE BADLY BAGEL BAKER BALER BALMY BALSA BANAL BARGE BASIC BASIN BASTE BATHE BATON BATTY BAWDY BAYOU BEACH BEADY BEAST BEAUT BEEFY BEGET BEGIN BEING BELCH BELIE BELLY BELOW BENCH BERET BERTH BESET BEVEL BICEP BILGE BINGE BIOME BIRCH BIRTH BLACK BLADE BLAME BLAND BLANK BLARE BLAZE BLEAK BLEED BLEEP BLIMP BLINK BLISS BLOCK BLOKE BLOND BLOWN BLUFF BLURB BLURT BLUSH BOARD BOAST BONGO BONUS BOOBY BOOST BOOTY BOOZE BOOZY BORAX BORNE BOSSY BOUGH BOXER BRACE BRAID BRAIN BRAKE BRAND BRASH BRASS BRAVE BRAVO BRAWN BREAD BREAK BREED BRIAR BRIBE BRIDE BRIEF BRINE BRING BRINK BRINY BRISK BROAD BROKE BROOK BROOM BROTH BROWN BRUSH BRUTE BUDDY BUGGY BUGLE BUILD BUILT BULKY BULLY BUNCH BURLY CABLE CACAO CACHE CADET CAMEL CAMEO CANDY CANNY CANOE CANON CAPER CARAT CARGO CAROL CARRY CARVE CATCH CATER CAULK CAUSE CEASE CEDAR CHAFE CHAIN CHALK CHAMP CHANT CHAOS CHARD CHARM CHART CHASE CHEAP CHEAT CHECK CHEEK CHEER CHEST CHIEF CHILD CHILL CHIME CHOCK CHOIR CHOKE CHORD CHORE CHOSE CHUNK CHUTE CIDER CIGAR CINCH CIRCA CIVIC CLASH CLASS CLEAN CLEAR CLEFT CLERK CLICK CLIMB CLING CLOAK CLOCK CLONE CLOSE CLOTH CLOUD CLOVE CLOWN CLUCK COACH COAST COCOA COLON COMET COMFY COMMA CONDO CONIC CORER CORNY COULD COUNT COURT COVER COVET COWER COYLY CRAFT CRAMP CRANE CRANK CRASS CRATE CRAVE CRAWL CRAZE CRAZY CREAK CREAM CREDO CREPE CREPT CREST CRIME CRIMP CRISP CROAK CRONE CROOK CROSS CROWD CROWN CRUMB CRUSH CRUST CRYPT CUMIN CURIO CURLY CURSE CURVE CYBER CYNIC DADDY DAISY DANCE DANDY DATUM DEATH DEBIT DEBUG DEBUT DECAL DECAY DECOY DECRY DEITY DELAY DELTA DELVE DENIM DEPOT DEPTH DETER DEVIL DIARY DICEY DIGIT DINER DINGO DINGY DIRGE DISCO DITTO DITTY DODGE DOGMA DOING DOLLY DONOR DONUT DOPEY DOUBT DOWEL DOWRY DOZEN DRAFT DRAIN DRAWN DREAD DREAM DRINK DRIVE DROLL DROOL DROOP DRONE DROVE DRYER DUCHY DUMMY DUTCH DUVET DWARF DWELL DWELT EAGER EAGLE EARLY EARTH EASEL EBONY EDICT EDIFY EGRET EJECT ELBOW ELDER ELITE ELOPE ELUDE EMAIL EMBER EMPTY ENACT ENDOW ENEMA ENJOY ENNUI ENSUE ENTER EPOCH EPOXY EQUAL EQUIP ERODE ERROR ERUPT ESSAY ETHER ETHIC ETHOS EVADE EVENT EVERY EVOKE EXACT EXALT EXCEL EXERT EXILE EXIST EXPEL EXTRA EXULT FACET FAINT FAITH FALSE FANCY FARCE FAULT FAVOR FEAST FEIGN FERAL FERRY FEVER FEWER FIBER FIELD FIEND FIFTH FIFTY FILET FINAL FINCH FINER FIRST FISHY FIXER FJORD FLAIL FLAIR FLAKE FLAME FLANK FLARE FLASH FLASK FLESH FLICK FLING FLINT FLIRT FLOAT FLOCK FLOOD FLOOR FLORA FLOSS FLOUR FLOUT FLOWN FLUFF FLUME FLUNG FLUNK FLYER FOAMY FOCAL FOCUS FOGGY FOIST FOLIO FOLLY FORAY FORCE FORGE FORGO FORTE FORTH FORTY FOUND FOYER FRAIL FRAME FRANK FRESH FRIED FROCK FROND FRONT FROST FROTH FROWN FROZE FULLY FUNGI FUNKY FUNNY FUZZY GAMER GAMMA GAMUT GAUDY GAUNT GAUZE GAWKY GECKO GENIE GENRE GHOST GHOUL GIANT GIDDY GIRTH GIVEN GLADE GLAND GLASS GLAZE GLEAM GLEAN GLIDE GLOAT GLOBE GLOOM GLORY GLOVE GLYPH GNASH GNOME GOING GOLEM GONER GOODY GOOFY GOOSE GORGE GOUGE GRACE GRADE GRAIL GRAIN GRAND GRANT GRAPH GRASP GRATE GREAT GREED GREEN GREET GRIEF GRIFT GRIME GRIMY GRIND GRIPE GROIN GROOM GROUP GROUT GROVE GROWL GROWN GRUEL GUANO GUARD GUEST GUIDE GUILD GUILE GULLY GUMMY GUPPY GUSTY HABIT HAIRY HALVE HANDY HAPPY HARSH HATCH HATER HAVOC HAZEL HEADY HEARD HEART HEATH HEAVE HEAVY HEFTY HEIST HELIX HELLO HENCE HERON HILLY HINGE HIPPO HITCH HOARD HOBBY HOMER HONEY HORDE HORSE HOTEL HOUND HOUSE HOVER HOWDY HUMAN HUMID HUMOR HUMPH HUNCH HUNKY HURRY HUTCH HYENA HYPER ICING IDIOM IDLER IGLOO IMAGE IMPEL INANE INBOX INCUR INDEX INDIE INEPT INERT INFER INLAY INNER INPUT INTER INTRO IONIC IRATE IRONY ISLET ITCHY IVORY JAUNT JAZZY JELLY JERKY JEWEL JIFFY JOINT JOKER JOLLY JOUST JUDGE JUICE JUMPY KARMA KAYAK KAZOO KEBAB KHAKI KIOSK KNACK KNAVE KNEAD KNEEL KNELT KNOCK KNOLL KNOWN KOALA KRILL LABEL LABOR LADLE LAGER LANKY LAPEL LAPSE LARGE LARVA LASER LASSO LATTE LAUGH LAYER LEAFY LEAKY LEAPT LEARN LEASE LEASH LEAVE LEDGE LEECH LEERY LEGGY LEMON LEMUR LIBEL LIGHT LILAC LIMIT LINEN LINER LINGO LITHE LIVER LIVID LOCAL LOCUS LODGE LOFTY LOGIC LOOPY LORIS LOSER LOUSE LOVER LOWER LOWLY LOYAL LUCID LUCKY LUNAR LUNCH LUNGE LUSTY LYING MACAW MACHO MADAM MADLY MAGIC MAGMA MAIZE MAJOR MAMBO MANGA MANGO MANIA MANLY MANOR MAPLE MARCH MARRY MARSH MASON MASSE MATCH MATEY MAUVE MAXIM MAYBE MAYOR MEALY MEANT MEDAL MEDIA MEDIC MELON MERCY MERGE MERIT MERRY METAL METER METRO MICRO MIDGE MIDST MIMIC MINCE MINER MINUS MODAL MODEL MODEM MOIST MOLAR MOLDY MOMMY MONEY MONTH MOOSE MORAL MOSSY MOTOR MOTTO MOULT MOUNT MOURN MOUSE MOVIE MUCKY MULCH MUMMY MUNCH MURAL MUSHY MUSIC MUSTY NAIVE NANNY NASTY NATAL NAVAL NAVEL NEEDY NEIGH NERDY NERVE NERVY NEVER NICER NICHE NIGHT NINJA NINTH NOBLE NOISE NORTH NOVEL NUDGE NURSE NYMPH OCCUR OCEAN OCTET ODDLY OFFAL OFFER OFTEN OLDER OLIVE ONION ONSET OPERA ORDER ORGAN OTHER OTTER OUGHT OUNCE OUTDO OUTER OVERT OWNER OXIDE OZONE PAINT PANEL PANIC PAPAL PAPER PARER PARRY PARTY PASTA PATCH PATIO PATSY PATTY PAUSE PEACE PEACH PEARL PEDAL PENNE PERCH PERKY PESKY PETTY PHASE PHONE PHONY PHOTO PIANO PICKY PIECE PIETY PILOT PINCH PINEY PINKY PINTO PIOUS PIPER PIQUE PITCH PITHY PIXEL PIXIE PLACE PLAID PLAIN PLAIT PLANK PLANT PLATE PLAZA PLEAT PLUCK PLUMB PLUNK POINT POISE POKER POLAR POLKA POLYP POPPY PORCH POUND POWER PRANK PREEN PRESS PRICE PRICK PRIDE PRIME PRIMO PRIMP PRINT PRIOR PRIZE PROBE PRONE PRONG PROSE PROUD PROVE PROWL PROXY PRUNE PSALM PULPY PUPIL PURGE QUAIL QUALM QUART QUASH QUEEN QUERY QUEST QUEUE QUICK QUIET QUIRK QUITE QUOTA QUOTE RADIO RAINY RAISE RAMEN RANCH RANGE RAPID RATIO RAYON REACH REACT READY REALM REBEL REBUS REBUT RECAP RECUR REFER REGAL RELAX RELIC RENEW REPAY REPEL RERUN RESIN RETCH RETRO RETRY REUSE REVEL REVUE RHINO RHYME RIDER RIDGE RIGHT RIPER RISEN RIVAL RIVET ROACH ROBIN ROBOT ROCKY RODEO ROGUE ROOMY ROUGE ROUGH ROUND ROUSE ROUTE ROVER ROWER ROYAL RUDDY RUDER RUMBA RUPEE RUSTY SAINT SALAD SALLY SALSA SALTY SANDY SASSY SAUCY SAUNA SAUTE SAVOR SCALD SCALE SCANT SCARE SCARF SCENT SCOFF SCOLD SCONE SCOPE SCORE SCORN SCOUR SCOUT SCOWL SCRAM SCRAP SCRUB SCRUM SEDAN SEEDY SENSE SERUM SERVE SEVEN SEVER SHADE SHAFT SHAKE SHAKY SHALL SHAME SHANK SHAPE SHARD SHARE SHARP SHAVE SHAWL SHEAR SHEET SHELF SHELL SHIFT SHINE SHIRE SHIRK SHORE SHORN SHOUT SHOVE SHOWN SHOWY SHRUB SHRUG SHUCK SHUNT SHUSH SHYLY SIEGE SIGHT SILLY SINCE SISSY SIXTH SKATE SKIER SKIFF SKILL SKIMP SKIRT SKUNK SLANG SLATE SLEEK SLEEP SLICE SLOPE SLOSH SLOTH SLUMP SLUNG SMALL SMART SMASH SMEAR SMELT SMILE SMIRK SMITE SMITH SMOCK SMOKE SNACK SNAFU SNAIL SNAKE SNAKY SNARE SNARL SNEAK SNOOP SNORT SNOUT SOGGY SOLAR SOLID SOLVE SONIC SORRY SOUND SOWER SPACE SPADE SPARE SPARK SPATE SPEAK SPEAR SPECK SPELL SPELT SPEND SPENT SPICE SPICY SPIEL SPIKE SPILL SPINE SPIRE SPITE SPLAT SPOKE SPOON SPORT SPOUT SPRAY SPRIG SPURT SQUAD SQUAT SQUID STAFF STAGE STAID STAIN STAIR STAKE STALE STALL STAMP STAND STARE STARK START STASH STATE STEAD STEAM STEED STEEL STEEP STEIN STERN STICK STIFF STILL STILT STING STINK STINT STOCK STOIC STOLE STOMP STONE STONY STOOD STOOL STORE STORM STORY STOUT STOVE STRAP STRAW STRAY STUDY STUMP STUNG STYLE SUAVE SUEDE SUGAR SUITE SULKY SUNNY SUPER SURER SURLY SUSHI SWATH SWEAT SWEEP SWEET SWELL SWILL SWINE SWIRL SWISH SWOON SWORD SWUNG SYRUP TABLE TABOO TACIT TACKY TAFFY TAKEN TALLY TALON TANGY TAPER TAPIR TARDY TASTE TASTY TAUNT TAUPE TAWNY TEACH TEARY TEASE TEMPO TENTH TEPID TERSE THANK THEIR THEME THERE THESE THIEF THIGH THING THINK THIRD THORN THOSE THREE THREW THROW THRUM THUMB THUMP THYME TIARA TIBIA TIDAL TIGER TILDE TIMER TIPSY TITAN TITHE TITLE TIZZY TOAST TODAY TONIC TOOTH TOPAZ TOPIC TORCH TORSO TOTAL TOTEM TOUCH TOUGH TOWEL TOXIC TOXIN TRACE TRACK TRACT TRADE TRAIL TRAIN TRAIT TRASH TRAWL TREAT TREND TRIAD TRICE TRIPE TRITE TROLL TROOP TROPE TROUT TROVE TRULY TRUSS TRUST TRUTH TRYST TUNIC TURBO TUTOR TWANG TWEAK TWEED TWICE TWINE TWIRL TWIST UDDER ULCER ULTRA UNCLE UNDER UNDID UNDUE UNFED UNFIT UNIFY UNITE UNLIT UNMET UNTIE UNTIL UNZIP UPPER UPSET URBAN USAGE USHER USING USUAL USURP UTTER UVULA VAGUE VALET VALID VALUE VAPID VAULT VENOM VERGE VERSE VERVE VIDEO VIGOR VILLA VINYL VIOLA VIRAL VISOR VITAL VIVID VIXEN VODKA VOICE VOILA VOTER VOUCH VYING WACKY WAFER WAGON WALTZ WASTE WATCH WEARY WEDGE WEEDY WEIRD WHACK WHALE WHEAT WHEEL WHELP WHERE WHICH WHIFF WHILE WHINE WHINY WHIRL WHISK WHOOP WHOSE WIDEN WINCE WINDY WITCH WITTY WOKEN WOMAN WOOER WORDY WORLD WORRY WORSE WORST WOULD WOVEN WRATH WREAK WRIST WRITE WRONG WROTE WRUNG YACHT YEARN YEAST YIELD YOUNG YOUTH ZEBRA ZESTY"""
used_words_list = [word.lower() for word in used_words.split(" ")]


success_round_count = 0
possibilities_left = []
round_count = 0

for idx in range(len(used_words_list)):
    black_chars = []
    green_chars = [None]*5
    yellow_chars = {}

    for i in range(5):
        yellow_chars[i] = []

    five_letter_words = persistent_five_letter_words.copy()
    answer = used_words_list[idx]
    sequence_of_guessing_words = []

    for att in range(6):
        match att:
            case 0:
                guessing_word = "salet"
            case _:
                ordered_list = sort_by_reference(five_letter_words_order_by_freq, five_letter_words)
                # guessing_word = random.choice(ordered_list[:min(len(ordered_list), max(1, 5-att//2))])
                guessing_word = ordered_list[0]

        sequence_of_guessing_words.append(guessing_word)

        green_chars_pos = []
        yellow_chars_pos = []

        to_be_implicited_yellow_chars = []
        for i in range(5):
            if answer[i] == guessing_word[i]:
                green_chars_pos.append(i)
            elif guessing_word[i] in answer and guessing_word[i] not in to_be_implicited_yellow_chars:
                yellow_chars_pos.append(i)
                to_be_implicited_yellow_chars.append(guessing_word[i])

        # green_chars_pos = "".join([str(i) for i in green_chars_pos])
        # yellow_chars_pos = "".join(str(i) for i in yellow_chars_pos)

        word_input = [i.lower() for i in guessing_word]

        # print(word_input)
        # print(answer)
        # print(green_chars_pos)
        # print(yellow_chars_pos)

        to_remove_chars = []
        for pos in green_chars_pos:
            green_chars[pos] = word_input[pos]
            to_remove_chars.append(word_input[pos])
            for item in yellow_chars:
                if word_input[pos] in yellow_chars[item]:
                    yellow_chars[item].remove(word_input[pos])

        implicit_yellow_chars = []
        for pos in yellow_chars_pos:
            if word_input[pos] in green_chars:
                to_remove_chars.append(word_input[pos])
                continue
            yellow_chars[pos] = list(set(yellow_chars[pos] + [word_input[pos]]))
            to_remove_chars.append(word_input[pos])
            implicit_yellow_chars.append(word_input[pos])

        for i in range(5):
            if word_input[i] in implicit_yellow_chars:
                yellow_chars[i] = list(set(yellow_chars[i] + [word_input[i]]))
            if green_chars[i]:
                yellow_chars[i] = []

        for char in to_remove_chars:
            word_input = [i for i in word_input if i != char]

        black_chars = list(set(black_chars + word_input))

        # print(black_chars)
        # print(yellow_chars)
        # print(green_chars)
        # print(five_letter_words, guessing_word, answer)

        five_letter_words = filter_words(black_chars, yellow_chars, green_chars, five_letter_words)
        if len(five_letter_words) == 1:
            break

        # print(five_letter_words, guessing_word, answer, att)

    if len(five_letter_words) == 1:
        success_round_count += 1
    else:
        possibilities_left.append(len(five_letter_words))
    round_count += 1

    if round_count % 100 == 0:
        if len(five_letter_words) == 1:
            print(f"Round {round_count} used {len(sequence_of_guessing_words)} attempts to guess the word \"{answer}\".")
        else:
            print(f"Round {round_count} used all 6 attempts but did not guess the word \"{answer}\". There are {len(five_letter_words)} possibilities left.")

        print(f"Sequence of guessing words: {', '.join(sequence_of_guessing_words)}")
        print(f"Success rate: {round(success_round_count / round_count * 100, 2)}%")
        print(f"Average possibilities left: {round(average(possibilities_left), 2)}")

print(f"Sequence of guessing words: {', '.join(sequence_of_guessing_words)}")
print(f"Success rate: {round(success_round_count / round_count * 100, 2)}%")
print(f"Average possibilities left: {round(average(possibilities_left), 2)}")
