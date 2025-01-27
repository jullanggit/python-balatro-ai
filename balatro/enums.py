from __future__ import annotations
from enum import Enum, auto
from functools import total_ordering


class JokerType(Enum):
    # Common - 61
    JOKER = "Joker"
    GREEDY_JOKER = "Greedy Joker"
    LUSTY_JOKER = "Lusty Joker"
    WRATHFUL_JOKER = "Wrathful Joker"
    GLUTTONOUS_JOKER = "Gluttonous Joker"
    JOLLY_JOKER = "Jolly Joker"
    ZANY_JOKER = "Zany Joker"
    MAD_JOKER = "Mad Joker"
    CRAZY_JOKER = "Crazy Joker"
    DROLL_JOKER = "Droll Joker"
    SLY_JOKER = "Sly Joker"
    WILY_JOKER = "Wily Joker"
    CLEVER_JOKER = "Clever Joker"
    DEVIOUS_JOKER = "Devious Joker"
    CRAFTY_JOKER = "Crafty Joker"
    HALF_JOKER = "Half Joker"
    CREDIT_CARD = "Credit Card"
    BANNER = "Banner"
    MYSTIC_SUMMIT = "Mystic Summit"
    EIGHT_BALL = "8 Ball"
    MISPRINT = "Misprint"
    RAISED_FIST = "Raised Fist"
    CHAOS_THE_CLOWN = "Chaos the Clown"
    SCARY_FACE = "Scary Face"
    ABSTRACT_JOKER = "Abstract Joker"
    DELAYED_GRATIFICATION = "Delayed Gratification"
    GROS_MICHEL = "Gros Michel"
    EVEN_STEVEN = "Even Steven"
    ODD_TODD = "Odd Todd"
    SCHOLAR = "Scholar"
    BUSINESS_CARD = "Business Card"
    SUPERNOVA = "Supernova"
    RIDE_THE_BUS = "Ride the Bus"
    EGG = "Egg"
    RUNNER = "Runner"
    ICE_CREAM = "Ice Cream"
    SPLASH = "Splash"
    BLUE_JOKER = "Blue Joker"
    FACELESS_JOKER = "Faceless Joker"
    GREEN_JOKER = "Green Joker"
    SUPERPOSITION = "Superposition"
    TODO_LIST = "To Do List"
    CAVENDISH = "Cavendish"
    RED_CARD = "Red Card"
    SQUARE_JOKER = "Square Joker"
    RIFF_RAFF = "Riff-Raff"
    PHOTOGRAPH = "Photograph"
    RESERVED_PARKING = "Reserved Parking"
    MAIL_IN_REBATE = "Mail-In Rebate"
    HALLUCINATION = "Hallucination"
    FORTUNE_TELLER = "Fortune Teller"
    JUGGLER = "Juggler"
    DRUNKARD = "Drunkard"
    GOLDEN_JOKER = "Golden Joker"
    POPCORN = "Popcorn"
    WALKIE_TALKIE = "Walkie Talkie"
    SMILEY_FACE = "Smiley Face"
    GOLDEN_TICKET = "Golden Ticket"
    SWASHBUCKLER = "Swashbuckler"
    HANGING_CHAD = "Hanging Chad"
    SHOOT_THE_MOON = "Shoot the Moon"
    # Uncommon - 64
    JOKER_STENCIL = "Joker Stencil"
    FOUR_FINGERS = "Four Fingers"
    MIME = "Mime"
    CEREMONIAL_DAGGER = "Ceremonial Dagger"
    MARBLE_JOKER = "Marble Joker"
    LOYALTY_CARD = "Loyalty Card"
    DUSK = "Dusk"
    FIBONACCI = "Fibonacci"
    STEEL_JOKER = "Steel Joker"
    HACK = "Hack"
    PAREIDOLIA = "Pareidolia"
    SPACE_JOKER = "Space Joker"
    BURGLAR = "Burglar"
    BLACKBOARD = "Blackboard"
    SIXTH_SENSE = "Sixth Sense"
    CONSTELLATION = "Constellation"
    HIKER = "Hiker"
    CARD_SHARP = "Card Sharp"
    MADNESS = "Madness"
    SEANCE = "Séance"
    VAMPIRE = "Vampire"
    SHORTCUT = "Shortcut"
    HOLOGRAM = "Hologram"
    CLOUD_NINE = "Cloud 9"
    ROCKET = "Rocket"
    MIDAS_MASK = "Midas Mask"
    LUCHADOR = "Luchador"
    GIFT_CARD = "Gift Card"
    TURTLE_BEAN = "Turtle Bean"
    EROSION = "Erosion"
    TO_THE_MOON = "To the Moon"
    STONE = "Stone Joker"
    LUCKY_CAT = "Lucky Cat"
    BULL = "Bull"
    DIET_COLA = "Diet Cola"
    TRADING_CARD = "Trading Card"
    FLASH_CARD = "Flash Card"
    SPARE_TROUSERS = "Spare Trousers"
    RAMEN = "Ramen"
    SELTZER = "Seltzer"
    CASTLE = "Castle"
    MR_BONES = "Mr. Bones"
    ACROBAT = "Acrobat"
    SOCK_AND_BUSKIN = "Sock and Buskin"
    TROUBADOUR = "Troubadour"
    CERTIFICATE = "Certificate"
    SMEARED_JOKER = "Smeared Joker"
    THROWBACK = "Throwback"
    ROUGH_GEM = "Rough Gem"
    BLOODSTONE = "Bloodstone"
    ARROWHEAD = "Arrowhead"
    ONYX_AGATE = "Onyx Agate"
    GLASS_JOKER = "Glass Joker"
    SHOWMAN = "Showman"
    FLOWER_POT = "Flower Pot"
    MERRY_ANDY = "Merry Andy"
    OOPS_ALL_SIXES = "Oops! All 6s"
    THE_IDOL = "The Idol"
    SEEING_DOUBLE = "Seeing Double"
    MATADOR = "Matador"
    SATELLITE = "Satellite"
    CARTOMANCER = "Cartomancer"
    ASTRONOMER = "Astronomer"
    BOOTSTRAPS = "Bootstraps"
    # Rare - 20
    DNA = "DNA"
    VAGABOND = "Vagabond"
    BARON = "Baron"
    OBELISK = "Obelisk"
    BASEBALL_CARD = "Baseball Card"
    ANCIENT_JOKER = "Ancient Joker"
    CAMPFIRE = "Campfire"
    BLUEPRINT = "Blueprint"
    WEE_JOKER = "Wee Joker"
    HIT_THE_ROAD = "Hit the Road"
    THE_DUO = "The Duo"
    THE_TRIO = "The Trio"
    THE_FAMILY = "The Family"
    THE_ORDER = "The Order"
    THE_TRIBE = "The Tribe"
    STUNTMAN = "Stuntman"
    INVISIBLE_JOKER = "Invisible Joker"
    BRAINSTORM = "Brainstorm"
    DRIVERS_LICENSE = "Driver's License"
    BURNT_JOKER = "Burnt Joker"
    # Legendary - 5
    CANIO = "Canio"
    TRIBOULET = "Triboulet"
    YORICK = "Yorick"
    CHICOT = "Chicot"
    PERKEO = "Perkeo"

    def __str__(self) -> str:
        return self.value


class Voucher(Enum):
    OVERSTOCK = "Overstock"
    CLEARANCE_SALE = "Clearance Sale"
    HONE = "Hone"
    REROLL_SURPLUS = "Reroll Surplus"
    CRYSTAL_BALL = "Crystal Ball"
    TELESCOPE = "Telescope"
    GRABBER = "Grabber"
    WASTEFUL = "Wasteful"
    TAROT_MERCHANT = "Tarot Merchant"
    PLANET_MERCHANT = "Planet Merchant"
    SEED_MONEY = "Seed Money"
    BLANK = "Blank"
    MAGIC_TRICK = "Magic Trick"
    HIEROGLYPH = "Hieroglyph"
    DIRECTORS_CUT = "Director's Cut"
    PAINT_BRUSH = "Paint Brush"
    OVERSTOCK_PLUS = "Overstock Plus"
    LIQUIDATION = "Liquidation"
    GLOW_UP = "Glow Up"
    REROLL_GLUT = "Reroll Glut"
    OMEN_GLOBE = "Omen Globe"
    OBSERVATORY = "Observatory"
    NACHO_TONG = "Nacho Tong"
    RECYCLOMANCY = "Recyclomancy"
    TAROT_TYCOON = "Tarot Tycoon"
    PLANET_TYCOON = "Planet Tycoon"
    MONEY_TREE = "Money Tree"
    ANTIMATTER = "Antimatter"
    ILLUSION = "Illusion"
    PETROGLYPH = "Petroglyph"
    RETCON = "Retcon"
    PALETTE = "Palette"

    def _repr_png_(self) -> bytes:
        from .sprites import get_sprite

        return get_sprite(self, as_image=False)


class Tarot(Enum):
    THE_FOOL = "The Fool"
    THE_MAGICIAN = "The Magician"
    THE_HIGH_PRIESTESS = "The High Priestess"
    THE_EMPRESS = "The Empress"
    THE_EMPEROR = "The Emperor"
    THE_HEIROPHANT = "The Hierophant"
    THE_LOVERS = "The Lovers"
    THE_CHARIOT = "The Chariot"
    JUSTICE = "Justice"
    THE_HERMIT = "The Hermit"
    THE_WHEEL_OF_FORTUNE = "The Wheel of Fortune"
    STRENGTH = "Strength"
    THE_HANGED_MAN = "The Hanged Man"
    DEATH = "Death"
    TEMPERANCE = "Temperance"
    THE_DEVIL = "The Devil"
    THE_TOWER = "The Tower"
    THE_STAR = "The Star"
    THE_MOON = "The Moon"
    THE_SUN = "The Sun"
    JUDGEMENT = "Judgement"
    THE_WORLD = "The World"


class Planet(Enum):
    ERIS = "Eris"
    CERES = "Ceres"
    PLANET_X = "Planet X"
    NEPTUNE = "Neptune"
    MARS = "Mars"
    EARTH = "Earth"
    JUPITER = "Jupiter"
    SATURN = "Saturn"
    VENUS = "Venus"
    URANUS = "Uranus"
    MERCURY = "Mercury"
    PLUTO = "Pluto"

    @property
    def poker_hand(self) -> Planet:
        return list(PokerHand)[list(Planet).index(self)]


class Spectral(Enum):
    FAMILIAR = "Familiar"
    GRIM = "Grim"
    INCANTATION = "Incantation"
    TALISMAN = "Talisman"
    AURA = "Aura"
    WRAITH = "Wraith"
    SIGIL = "Sigil"
    OUIJA = "Ouija"
    ECTOPLASM = "Ectoplasm"
    IMMOLATE = "Immolate"
    ANKH = "Ankh"
    DEJA_VU = "Deja Vu"
    HEX = "Hex"
    TRANCE = "Trance"
    MEDIUM = "Medium"
    CRYPTID = "Cryptid"
    THE_SOUL = "The Soul"
    BLACK_HOLE = "Black Hole"


class Edition(Enum):
    BASE = "Base"
    FOIL = "Foil"
    HOLO = "Holographic"
    POLYCHROME = "Polychrome"
    NEGATIVE = "Negative"


class Enhancement(Enum):
    BONUS = "Bonus"
    MULT = "Mult"
    WILD = "Wild"
    GLASS = "Glass"
    STEEL = "Steel"
    STONE = "Stone"
    GOLD = "Gold"
    LUCKY = "Lucky"


@total_ordering
class Stake(Enum):
    GOLD = "Gold"
    ORANGE = "Orange"
    PURPLE = "Purple"
    BLUE = "Blue"
    BLACK = "Black"
    GREEN = "Green"
    RED = "Red"
    WHITE = "White"

    def __lt__(self, other: Stake) -> bool:
        match other:
            case Stake():
                return list(Stake).index(self) > list(Stake).index(other)

        return NotImplemented

    def _repr_png_(self) -> bytes:
        from .sprites import get_sprite

        return get_sprite(self, as_image=False)


class Tag(Enum):
    UNCOMMON = "Uncommon Tag"
    RARE = "Rare Tag"
    NEGATIVE = "Negative Tag"
    FOIL = "Foil Tag"
    HOLOGRAPHIC = "Holographic Tag"
    POLYCHROME = "Polychrome Tag"
    INVESTMENT = "Investment Tag"
    VOUCHER = "Voucher Tag"
    BOSS = "Boss Tag"
    STANDARD = "Standard Tag"
    CHARM = "Charm Tag"
    METEOR = "Meteor Tag"
    BUFFOON = "Buffoon Tag"
    HANDY = "Handy Tag"
    GARBAGE = "Garbage Tag"
    COUPON = "Coupon Tag"
    DOUBLE = "Double Tag"
    JUGGLE = "Juggle Tag"
    DSIX = "D6 Tag"
    TOP_UP = "Top-up Tag"
    SPEED = "Speed Tag"
    ORBITAL = "Orbital Tag"
    ECONOMY = "Economy Tag"
    ETHEREAL = "Ethereal Tag"

    def _repr_png_(self) -> bytes:
        from .sprites import get_sprite

        return get_sprite(self, as_image=False)


class Blind(Enum):
    SMALL_BLIND = "Small Blind"
    BIG_BLIND = "Big Blind"
    THE_HOOK = "The Hook"
    THE_WALL = "The Wall"
    THE_WHEEL = "The Wheel"
    THE_ARM = "The Arm"
    THE_PSYCHIC = "The Psychic"
    THE_GOAD = "The Goad"
    THE_WATER = "The Water"
    THE_EYE = "The Eye"
    THE_MOUTH = "The Mouth"
    THE_PLANT = "The Plant"
    THE_NEEDLE = "The Needle"
    THE_HEAD = "The Head"
    THE_TOOTH = "The Tooth"
    THE_OX = "The Ox"
    THE_HOUSE = "The House"
    THE_CLUB = "The Club"
    THE_FISH = "The Fish"
    THE_WINDOW = "The Window"
    THE_MANACLE = "The Manacle"
    THE_SERPENT = "The Serpent"
    THE_PILLAR = "The Pillar"
    THE_FLINT = "The Flint"
    THE_MARK = "The Mark"
    AMBER_ACORN = "Amber Acorn"
    CRIMSON_HEART = "Crimson Heart"
    CERULEAN_BELL = "Cerulean Bell"
    VERDANT_LEAF = "Verdant Leaf"
    VIOLET_VESSEL = "Violet Vessel"

    def _repr_png_(self) -> bytes:
        from .sprites import get_sprite

        return get_sprite(self, as_image=False)


class Deck(Enum):
    RED = "Red"
    BLUE = "Blue"
    YELLOW = "Yellow"
    GREEN = "Green"
    BLACK = "Black"
    MAGIC = "Magic"
    NEBULA = "Nebula"
    GHOST = "Ghost"
    ABANDONED = "Abandoned"
    CHECKERED = "Checkered"
    ZODIAC = "Zodiac"
    PAINTED = "Painted"
    ANAGLYPH = "Anaglyph"
    PLASMA = "Plasma"
    ERRATIC = "Erratic"

    def _repr_png_(self) -> bytes:
        from .sprites import get_sprite

        return get_sprite(self, as_image=False)

    @property
    def starting_size(self) -> int:
        return 40 if self is Deck.ABANDONED else 52


class Seal(Enum):
    GOLD = "Gold"
    RED = "Red"
    BLUE = "Blue"
    PURPLE = "Purple"


class Pack(Enum):
    ARCANA = "Arcana Pack"
    JUMBO_ARCANA = "Jumbo Arcana Pack"
    MEGA_ARCANA = "Mega Arcana Pack"
    CELESTIAL = "Celestial Pack"
    JUMBO_CELESTIAL = "Jumbo Celestial Pack"
    MEGA_CELESTIAL = "Mega Celestial Pack"
    SPECTRAL = "Spectral Pack"
    JUMBO_SPECTRAL = "Jumbo Spectral Pack"
    MEGA_SPECTRAL = "Mega Spectral Pack"
    STANDARD = "Standard Pack"
    JUMBO_STANDARD = "Jumbo Standard Pack"
    MEGA_STANDARD = "Mega Standard Pack"
    BUFFOON = "Buffoon Pack"
    JUMBO_BUFFOON = "Jumbo Buffoon Pack"
    MEGA_BUFFOON = "Mega Buffoon Pack"

    def _repr_png_(self) -> bytes:
        from .sprites import get_sprite

        return get_sprite(self, as_image=False)


class Suit(Enum):
    SPADES = "Spades"
    HEARTS = "Hearts"
    CLUBS = "Clubs"
    DIAMONDS = "Diamonds"

    def __str__(self) -> str:
        return self.value


@total_ordering
class Rank(Enum):
    ACE = "Ace"
    KING = "King"
    QUEEN = "Queen"
    JACK = "Jack"
    TEN = "10"
    NINE = "9"
    EIGHT = "8"
    SEVEN = "7"
    SIX = "6"
    FIVE = "5"
    FOUR = "4"
    THREE = "3"
    TWO = "2"

    def __int__(self) -> int:
        return 14 - list(Rank).index(self)

    def __lt__(self, other: Rank) -> bool:
        match other:
            case Rank():
                return list(Rank).index(self) > list(Rank).index(other)

        return NotImplemented

    def __str__(self) -> str:
        return self.value

    @property
    def chips(self) -> int:
        if self is Rank.ACE:
            return 11
        elif self.is_face:
            return 10
        else:
            return int(self)

    @property
    def is_face(self) -> bool:
        return self in [Rank.KING, Rank.QUEEN, Rank.JACK]


@total_ordering
class PokerHand(Enum):
    FLUSH_FIVE = "Flush Five"
    FLUSH_HOUSE = "Flush House"
    FIVE_OF_A_KIND = "Five of a Kind"
    STRAIGHT_FLUSH = "Straight Flush"
    FOUR_OF_A_KIND = "Four of a Kind"
    FULL_HOUSE = "Full House"
    FLUSH = "Flush"
    STRAIGHT = "Straight"
    THREE_OF_A_KIND = "Three of a Kind"
    TWO_PAIR = "Two Pair"
    PAIR = "Pair"
    HIGH_CARD = "High Card"

    def __lt__(self, other: PokerHand) -> bool:
        match other:
            case PokerHand():
                return list(PokerHand).index(self) > list(PokerHand).index(other)

        return NotImplemented

    def __str__(self) -> str:
        return self.value

    @property
    def planet(self) -> Planet:
        return list(Planet)[list(PokerHand).index(self)]


class Rarity(Enum):
    COMMON = "Common"
    UNCOMMON = "Uncommon"
    RARE = "Rare"
    LEGENDARY = "Legendary"


class Challenge(Enum):
    THE_OMELETTE = "The Omelette"
    FIFTEEN_MINUTE_CITY = "15 Minute City"
    RICH_GET_RICHER = "Rich get Richer"
    ON_A_KNIFES_EDGE = "On a Knife's Edge"
    X_RAY_VISION = "X-ray Vision"
    MAD_WORLD = "Mad World"
    LUXURY_TAX = "Luxury Tax"
    NON_PERISHABLE = "Non-Perishable"
    MEDUSA = "Medusa"
    DOUBLE_OR_NOTHING = "Double or Nothing"
    TYPECAST = "Typecast"
    INFLATION = "Inflation"
    BRAM_POKER = "Bram Poker"
    FRAGILE = "Fragile"
    MONOLITH = "Monolith"
    BLAST_OFF = "Blast Off"
    FIVE_CARD_DRAW = "Five-Card Draw"
    GOLDEN_NEEDLE = "Golden Needle"
    CRUELTY = "Cruelty"
    JOKERLESS = "Jokerless"


class State(Enum):
    CASHING_OUT = auto()
    GAME_OVER = auto()
    IN_SHOP = auto()
    OPENING_PACK = auto()
    PLAYING_BLIND = auto()
    SELECTING_BLIND = auto()
