from __future__ import annotations
from enum import Enum, auto


class JokerType(Enum):
    # Common - 61
    JOKER = "Joker"
    GREEDY_JOKER = "Greedy Joker"
    LUSTY_JOKER = "Lusty Joker"
    WRATHFUL_JOKER = "Wrathful Joker"
    GLUTTENOUS_JOKER = "Gluttonous Joker"
    JOLLY = "Jolly Joker"
    ZANY = "Zany Joker"
    MAD = "Mad Joker"
    CRAZY = "Crazy Joker"
    DROLL = "Droll Joker"
    SLY = "Sly Joker"
    WILY = "Wily Joker"
    CLEVER = "Clever Joker"
    DEVIOUS = "Devious Joker"
    CRAFTY = "Crafty Joker"
    HALF = "Half Joker"
    CREDIT_CARD = "Credit Card"
    BANNER = "Banner"
    MYSTIC_SUMMIT = "Mystic Summit"
    EIGHT_BALL = "8 Ball"
    MISPRINT = "Misprint"
    RAISED_FIST = "Raised Fist"
    CHAOS = "Chaos the Clown"
    SCARY_FACE = "Scary Face"
    ABSTRACT = "Abstract Joker"
    DELAYED_GRAT = "Delayed Gratification"
    GROS_MICHEL = "Gros Michel"
    EVEN_STEVEN = "Even Steven"
    ODD_TODD = "Odd Todd"
    SCHOLAR = "Scholar"
    BUSINESS = "Business Card"
    SUPERNOVA = "Supernova"
    RIDE_THE_BUS = "Ride the Bus"
    EGG = "Egg"
    RUNNER = "Runner"
    ICE_CREAM = "Ice Cream"
    SPLASH = "Splash"
    BLUE_JOKER = "Blue Joker"
    FACELESS = "Faceless Joker"
    GREEN_JOKER = "Green Joker"
    SUPERPOSITION = "Superposition"
    TODO_LIST = "To Do List"
    CAVENDISH = "Cavendish"
    RED_CARD = "Red Card"
    SQUARE = "Square Joker"
    RIFF_RAFF = "Riff-Raff"
    PHOTOGRAPH = "Photograph"
    RESERVED_PARKING = "Reserved Parking"
    MAIL = "Mail-In Rebate"
    HALLUCINATION = "Hallucination"
    FORTUNE_TELLER = "Fortune Teller"
    JUGGLER = "Juggler"
    DRUNKARD = "Drunkard"
    GOLDEN = "Golden Joker"
    POPCORN = "Popcorn"
    WALKIE_TALKIE = "Walkie Talkie"
    SMILEY = "Smiley Face"
    TICKET = "Golden Ticket"
    SWASHBUCKLER = "Swashbuckler"
    HANGING_CHAD = "Hanging Chad"
    SHOOT_THE_MOON = "Shoot the Moon"
    # Uncommon - 64
    STENCIL = "Joker Stencil"
    FOUR_FINGERS = "Four Fingers"
    MIME = "Mime"
    CEREMONIAL = "Ceremonial Dagger"
    MARBLE = "Marble Joker"
    LOYALTY_CARD = "Loyalty Card"
    DUSK = "Dusk"
    FIBONACCI = "Fibonacci"
    STEEL_JOKER = "Steel Joker"
    HACK = "Hack"
    PAREIDOLIA = "Pareidolia"
    SPACE = "Space Joker"
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
    CLOUD_9 = "Cloud 9"
    ROCKET = "Rocket"
    MIDAS_MASK = "Midas Mask"
    LUCHADOR = "Luchador"
    GIFT = "Gift Card"
    TURTLE_BEAN = "Turtle Bean"
    EROSION = "Erosion"
    TO_THE_MOON = "To the Moon"
    STONE = "Stone Joker"
    LUCKY_CAT = "Lucky Cat"
    BULL = "Bull"
    DIET_COLA = "Diet Cola"
    TRADING = "Trading Card"
    FLASH = "Flash Card"
    TROUSERS = "Spare Trousers"
    RAMEN = "Ramen"
    SELTZER = "Seltzer"
    CASTLE = "Castle"
    MR_BONES = "Mr. Bones"
    ACROBAT = "Acrobat"
    SOCK_AND_BUSKIN = "Sock and Buskin"
    TROUBADOUR = "Troubadour"
    CERTIFICATE = "Certificate"
    SMEARED = "Smeared Joker"
    THROWBACK = "Throwback"
    ROUGH_GEM = "Rough Gem"
    BLOODSTONE = "Bloodstone"
    ARROWHEAD = "Arrowhead"
    ONYX_AGATE = "Onyx Agate"
    GLASS = "Glass Joker"
    RING_MASTER = "Showman"
    FLOWER_POT = "Flower Pot"
    MERRY_ANDY = "Merry Andy"
    OOPS = "Oops! All 6s"
    IDOL = "The Idol"
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
    BASEBALL = "Baseball Card"
    ANCIENT = "Ancient Joker"
    CAMPFIRE = "Campfire"
    BLUEPRINT = "Blueprint"
    WEE = "Wee Joker"
    HIT_THE_ROAD = "Hit the Road"
    DUO = "The Duo"
    TRIO = "The Trio"
    FAMILY = "The Family"
    ORDER = "The Order"
    TRIBE = "The Tribe"
    STUNTMAN = "Stuntman"
    INVISIBLE = "Invisible Joker"
    BRAINSTORM = "Brainstorm"
    DRIVERS_LICENSE = "Driver's License"
    BURNT = "Burnt Joker"
    # Legendary - 5
    CANIO = "Canio"
    TRIBOULET = "Triboulet"
    YORICK = "Yorick"
    CHICOT = "Chicot"
    PERKEO = "Perkeo"


class Voucher(Enum):
    OVERSTOCK_NORM = "Overstock"
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
        from balatro_resources import get_sprite

        return get_sprite(self, False)


class Tarot(Enum):
    FOOL = "The Fool"
    MAGICIAN = "The Magician"
    HIGH_PRIESTESS = "The High Priestess"
    EMPRESS = "The Empress"
    EMPEROR = "The Emperor"
    HEIROPHANT = "The Hierophant"
    LOVERS = "The Lovers"
    CHARIOT = "The Chariot"
    JUSTICE = "Justice"
    HERMIT = "The Hermit"
    WHEEL_OF_FORTUNE = "The Wheel of Fortune"
    STRENGTH = "Strength"
    HANGED_MAN = "The Hanged Man"
    DEATH = "Death"
    TEMPERANCE = "Temperance"
    DEVIL = "The Devil"
    TOWER = "The Tower"
    STAR = "The Star"
    MOON = "The Moon"
    SUN = "The Sun"
    JUDGEMENT = "Judgement"
    WORLD = "The World"


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
    SOUL = "The Soul"
    BLACK_HOLE = "Black Hole"


class Edition(Enum):
    BASE = "Base"
    FOIL = "Foil"
    HOLO = "Holographic"
    POLYCHROME = "Polychrome"
    NEGATIVE = "Negative"


class Enhancement(Enum):
    BONUS = "Bonus Card"
    MULT = "Mult Card"
    WILD = "Wild Card"
    GLASS = "Glass Card"
    STEEL = "Steel Card"
    STONE = "Stone Card"
    GOLD = "Gold Card"
    LUCKY = "Lucky Card"


class Stake(Enum):
    WHITE = "White Stake"
    RED = "Red Stake"
    GREEN = "Green Stake"
    BLUE = "Blue Stake"
    BLACK = "Black Stake"
    PURPLE = "Purple Stake"
    ORANGE = "Orange Stake"
    GOLD = "Gold Stake"


class Tag(Enum):
    UNCOMMON = "Uncommon Tag"
    RARE = "Rare Tag"
    NEGATIVE = "Negative Tag"
    FOIL = "Foil Tag"
    HOLO = "Holographic Tag"
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
    D_SIX = "D6 Tag"
    TOP_UP = "Top-up Tag"
    SKIP = "Speed Tag"
    ORBITAL = "Orbital Tag"
    ECONOMY = "Economy Tag"
    ETHEREAL = "Ethereal Tag"


class Blind(Enum):
    SMALL = "Small Blind"
    BIG = "Big Blind"
    HOOK = "The Hook"
    WALL = "The Wall"
    WHEEL = "The Wheel"
    ARM = "The Arm"
    PSYCHIC = "The Psychic"
    GOAD = "The Goad"
    WATER = "The Water"
    EYE = "The Eye"
    MOUTH = "The Mouth"
    PLANT = "The Plant"
    NEEDLE = "The Needle"
    HEAD = "The Head"
    TOOTH = "The Tooth"
    FINAL_LEAF = "Verdant Leaf"
    FINAL_VESSEL = "Violet Vessel"
    OX = "The Ox"
    HOUSE = "The House"
    CLUB = "The Club"
    FISH = "The Fish"
    WINDOW = "The Window"
    MANACLE = "The Manacle"
    SERPENT = "The Serpent"
    PILLAR = "The Pillar"
    FLINT = "The Flint"
    MARK = "The Mark"
    FINAL_ACORN = "Amber Acorn"
    FINAL_HEART = "Crimson Heart"
    FINAL_BELL = "Cerulean Bell"


class Deck(Enum):
    RED = "Red Deck"
    BLUE = "Blue Deck"
    YELLOW = "Yellow Deck"
    GREEN = "Green Deck"
    BLACK = "Black Deck"
    MAGIC = "Magic Deck"
    NEBULA = "Nebula Deck"
    GHOST = "Ghost Deck"
    ABANDONED = "Abandoned Deck"
    CHECKERED = "Checkered Deck"
    ZODIAC = "Zodiac Deck"
    PAINTED = "Painted Deck"
    ANAGLYPH = "Anaglyph Deck"
    PLASMA = "Plasma Deck"
    ERRATIC = "Erratic Deck"
    CHALLENGE = "Challenge Deck"


class Seal(Enum):
    GOLD_SEAL = "Gold Seal"
    RED_SEAL = "Red Seal"
    BLUE_SEAL = "Blue Seal"
    PURPLE_SEAL = "Purple Seal"


class Pack(Enum):
    ARCANA_NORMAL = "Arcana Pack"
    ARCANA_JUMBO = "Jumbo Arcana Pack"
    ARCANA_MEGA = "Mega Arcana Pack"
    CELESTIAL_NORMAL = "Celestial Pack"
    CELESTIAL_JUMBO = "Jumbo Celestial Pack"
    CELESTIAL_MEGA = "Mega Celestial Pack"
    SPECTRAL_NORMAL = "Spectral Pack"
    SPECTRAL_JUMBO = "Jumbo Spectral Pack"
    SPECTRAL_MEGA = "Mega Spectral Pack"
    STANDARD_NORMAL = "Standard Pack"
    STANDARD_JUMBO = "Jumbo Standard Pack"
    STANDARD_MEGA = "Mega Standard Pack"
    BUFFOON_NORMAL = "Buffoon Pack"
    BUFFOON_JUMBO = "Jumbo Buffoon Pack"
    BUFFOON_MEGA = "Mega Buffoon Pack"

    def _repr_png_(self) -> bytes:
        from balatro_resources import get_sprite

        return get_sprite(self, False)


class Suit(Enum):
    SPADES = "Spades"
    HEARTS = "Hearts"
    CLUBS = "Clubs"
    DIAMONDS = "Diamonds"


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
        return 14 - list(self.__class__).index(self)

    def __lt__(self, other: Rank) -> bool:
        if isinstance(other, Rank):
            return int(self) < int(other)
        return NotImplemented

    @property
    def chips(self) -> int:
        if self is Rank.ACE:
            return 11
        elif self in [Rank.KING, Rank.QUEEN, Rank.JACK]:
            return 10
        else:
            return int(self)


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

    @property
    def planet(self) -> Planet:
        return list(Planet)[list(self.__class__).index(self)]


class Rarity(Enum):
    COMMON = auto()
    UNCOMMON = auto()
    RARE = auto()
    LEGENDARY = auto()


class State(Enum):
    SELECTING_BLIND = auto()
    PLAYING_BLIND = auto()
    IN_SHOP = auto()
    OPENING_PACK_SHOP = auto()
    OPENING_PACK_TAG = auto()
