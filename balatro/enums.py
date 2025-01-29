from __future__ import annotations
from enum import Enum, auto
from functools import total_ordering


# TODO: remove
class JokerType(Enum):
    # Common - 61
    Joker = "Joker"
    GreedyJoker = "Greedy Joker"
    LustyJoker = "Lusty Joker"
    WrathfulJoker = "Wrathful Joker"
    GluttonousJoker = "Gluttonous Joker"
    JollyJoker = "Jolly Joker"
    ZanyJoker = "Zany Joker"
    MadJoker = "Mad Joker"
    CrazyJoker = "Crazy Joker"
    DrollJoker = "Droll Joker"
    SlyJoker = "Sly Joker"
    WilyJoker = "Wily Joker"
    CleverJoker = "Clever Joker"
    DeviousJoker = "Devious Joker"
    CraftyJoker = "Crafty Joker"
    HalfJoker = "Half Joker"
    CreditCard = "Credit Card"
    Banner = "Banner"
    MysticSummit = "Mystic Summit"
    EightBall = "8 Ball"
    Misprint = "Misprint"
    RaisedFist = "Raised Fist"
    ChaosTheClown = "Chaos the Clown"
    ScaryFace = "Scary Face"
    AbstractJoker = "Abstract Joker"
    DelayedGratification = "Delayed Gratification"
    GrosMichel = "Gros Michel"
    EvenSteven = "Even Steven"
    OddTodd = "Odd Todd"
    Scholar = "Scholar"
    BusinessCard = "Business Card"
    Supernova = "Supernova"
    RideTheBus = "Ride the Bus"
    Egg = "Egg"
    Runner = "Runner"
    IceCream = "Ice Cream"
    Splash = "Splash"
    BlueJoker = "Blue Joker"
    FacelessJoker = "Faceless Joker"
    GreenJoker = "Green Joker"
    Superposition = "Superposition"
    ToDoList = "To Do List"
    Cavendish = "Cavendish"
    RedCard = "Red Card"
    SquareJoker = "Square Joker"
    RiffRaff = "Riff-Raff"
    Photograph = "Photograph"
    ReservedParking = "Reserved Parking"
    MailInRebate = "Mail-In Rebate"
    Hallucination = "Hallucination"
    FortuneTeller = "Fortune Teller"
    Juggler = "Juggler"
    Drunkard = "Drunkard"
    GoldenJoker = "Golden Joker"
    Popcorn = "Popcorn"
    WalkieTalkie = "Walkie Talkie"
    SmileyFace = "Smiley Face"
    GoldenTicket = "Golden Ticket"
    Swashbuckler = "Swashbuckler"
    HangingChad = "Hanging Chad"
    ShootTheMoon = "Shoot the Moon"
    # Uncommon - 64
    JokerStencil = "Joker Stencil"
    FourFingers = "Four Fingers"
    Mime = "Mime"
    CeremonialDagger = "Ceremonial Dagger"
    MarbleJoker = "Marble Joker"
    LoyaltyCard = "Loyalty Card"
    Dusk = "Dusk"
    Fibonacci = "Fibonacci"
    SteelJoker = "Steel Joker"
    Hack = "Hack"
    Pareidolia = "Pareidolia"
    SpaceJoker = "Space Joker"
    Burglar = "Burglar"
    Blackboard = "Blackboard"
    SixthSense = "Sixth Sense"
    Constellation = "Constellation"
    Hiker = "Hiker"
    CardSharp = "Card Sharp"
    Madness = "Madness"
    Seance = "Séance"
    Vampire = "Vampire"
    Shortcut = "Shortcut"
    Hologram = "Hologram"
    CloudNine = "Cloud 9"
    Rocket = "Rocket"
    MidasMask = "Midas Mask"
    Luchador = "Luchador"
    GiftCard = "Gift Card"
    TurtleBean = "Turtle Bean"
    Erosion = "Erosion"
    ToTheMoon = "To the Moon"
    StoneJoker = "Stone Joker"
    LuckyCat = "Lucky Cat"
    Bull = "Bull"
    DietCola = "Diet Cola"
    TradingCard = "Trading Card"
    FlashCard = "Flash Card"
    SpareTrousers = "Spare Trousers"
    Ramen = "Ramen"
    Seltzer = "Seltzer"
    Castle = "Castle"
    MrBones = "Mr. Bones"
    Acrobat = "Acrobat"
    SockAndBuskin = "Sock and Buskin"
    Troubadour = "Troubadour"
    Certificate = "Certificate"
    SmearedJoker = "Smeared Joker"
    Throwback = "Throwback"
    RoughGem = "Rough Gem"
    Bloodstone = "Bloodstone"
    Arrowhead = "Arrowhead"
    OnyxAgate = "Onyx Agate"
    GlassJoker = "Glass Joker"
    Showman = "Showman"
    FlowerPot = "Flower Pot"
    MerryAndy = "Merry Andy"
    OopsAllSixes = "Oops! All 6s"
    TheIdol = "The Idol"
    SeeingDouble = "Seeing Double"
    Matador = "Matador"
    Satellite = "Satellite"
    Cartomancer = "Cartomancer"
    Astronomer = "Astronomer"
    Bootstraps = "Bootstraps"
    # Rare - 20
    DNA = "DNA"
    Vagabond = "Vagabond"
    Baron = "Baron"
    Obelisk = "Obelisk"
    BaseballCard = "Baseball Card"
    AncientJoker = "Ancient Joker"
    Campfire = "Campfire"
    Blueprint = "Blueprint"
    WeeJoker = "Wee Joker"
    HitTheRoad = "Hit the Road"
    TheDuo = "The Duo"
    TheTrio = "The Trio"
    TheFamily = "The Family"
    TheOrder = "The Order"
    TheTribe = "The Tribe"
    Stuntman = "Stuntman"
    InvisibleJoker = "Invisible Joker"
    Brainstorm = "Brainstorm"
    DriversLicense = "Driver's License"
    BurntJoker = "Burnt Joker"
    # Legendary - 5
    Canio = "Canio"
    Triboulet = "Triboulet"
    Yorick = "Yorick"
    Chicot = "Chicot"
    Perkeo = "Perkeo"

    DEFAULT = Joker


class Voucher(Enum):
    OVERSTOCK = "Overstock"
    """
    +1 card slot available in shop
    """
    CLEARANCE_SALE = "Clearance Sale"
    """
    All cards and packs in shop are 25% off
    """
    HONE = "Hone"
    """
    Foil, Holographic, and Polychrome cards appear 2x more often
    """
    REROLL_SURPLUS = "Reroll Surplus"
    """
    Rerolls cost $2 less
    """
    CRYSTAL_BALL = "Crystal Ball"
    """
    +1 consumable slot
    """
    TELESCOPE = "Telescope"
    """
    Celestial Packs always contain the Planet card for your most played poker hand
    """
    GRABBER = "Grabber"
    """
    Permanently gain +1 hand per round
    """
    WASTEFUL = "Wasteful"
    """
    Permanently gain +1 discard each round
    """
    TAROT_MERCHANT = "Tarot Merchant"
    """
    Tarot cards appear 2X more frequently in the shop
    """
    PLANET_MERCHANT = "Planet Merchant"
    """
    Planet cards appear 2X more frequently in the shop
    """
    SEED_MONEY = "Seed Money"
    """
    Raise the cap on interest earned in each round to $10
    """
    BLANK = "Blank"
    """
    Does nothing?
    """
    MAGIC_TRICK = "Magic Trick"
    """
    Playing cards can be purchased from the shop
    """
    HIEROGLYPH = "Hieroglyph"
    """
    -1 Ante,
    -1 hand each round
    """
    DIRECTORS_CUT = "Director's Cut"
    """
    Reroll Boss Blind 1 time per Ante, $10 per roll
    """
    PAINT_BRUSH = "Paint Brush"
    """
    +1 hand size
    """
    OVERSTOCK_PLUS = "Overstock Plus"
    """
    +1 card slot available in shop
    """
    LIQUIDATION = "Liquidation"
    """
    All cards and packs in shop are 50% off
    """
    GLOW_UP = "Glow Up"
    """
    Foil, Holographic, and Polychrome cards appear 4x more often
    """
    REROLL_GLUT = "Reroll Glut"
    """
    Rerolls cost $2 less
    """
    OMEN_GLOBE = "Omen Globe"
    """
    Spectral cards may appear in any of the Arcana Packs
    """
    OBSERVATORY = "Observatory"
    """
    Planet cards in your consumable area give X1.5 Mult for their specified poker hand
    """
    NACHO_TONG = "Nacho Tong"
    """
    Permanently gain +1 hand per round
    """
    RECYCLOMANCY = "Recyclomancy"
    """
    Permanently gain +1 discard each round
    """
    TAROT_TYCOON = "Tarot Tycoon"
    """
    Tarot cards appear 4X more frequently in the shop
    """
    PLANET_TYCOON = "Planet Tycoon"
    """
    Planet cards appear 4X more frequently in the shop
    """
    MONEY_TREE = "Money Tree"
    """
    Raise the cap on interest earned in each round to $20
    """
    ANTIMATTER = "Antimatter"
    """
    +1 Joker slot
    """
    ILLUSION = "Illusion"
    """
    Playing cards in shop may have an Enhancement, Edition, and/or a Seal
    """
    PETROGLYPH = "Petroglyph"
    """
    -1 Ante,
    -1 discard each round
    """
    RETCON = "Retcon"
    """
    Reroll Boss Blind unlimited times, $10 per roll
    """
    PALETTE = "Palette"
    """
    +1 hand size
    """

    def _repr_png_(self) -> bytes:
        from .sprites import get_sprite

        return get_sprite(self, as_image=False)


class Tarot(Enum):
    THE_FOOL = "The Fool"
    """
    Creates the last Tarot or Planet card used during this run
    The Fool excluded
    """
    THE_MAGICIAN = "The Magician"
    """
    Enhances 2 selected cards to Lucky Cards
    """
    THE_HIGH_PRIESTESS = "The High Priestess"
    """
    Creates up to 2 random Planet cards
    (Must have room)
    """
    THE_EMPRESS = "The Empress"
    """
    Enhances 2 selected cards to Mult Cards
    """
    THE_EMPEROR = "The Emperor"
    """
    Creates up to 2 random Tarot cards
    (Must have room)
    """
    THE_HEIROPHANT = "The Hierophant"
    """
    Enhances 2 selected cards to Bonus Cards
    """
    THE_LOVERS = "The Lovers"
    """
    Enhances 1 selected card into a Wild Card
    """
    THE_CHARIOT = "The Chariot"
    """
    Enhances 1 selected card into a Steel Card
    """
    JUSTICE = "Justice"
    """
    Enhances 1 selected card into a Glass Card
    """
    THE_HERMIT = "The Hermit"
    """
    Doubles money
    (Max of $20)
    """
    THE_WHEEL_OF_FORTUNE = "The Wheel of Fortune"
    """
    1 in 4 chance to add Foil, Holographic, or Polychrome edition to a random Joker
    """
    STRENGTH = "Strength"
    """
    Increases rank of up to 2 selected cards by 1
    """
    THE_HANGED_MAN = "The Hanged Man"
    """
    Destroys up to 2 selected cards
    """
    DEATH = "Death"
    """
    Select 2 cards, convert the left card into the right card
    """
    TEMPERANCE = "Temperance"
    """
    Gives the total sell value of all current Jokers
    (Max of $50)
    """
    THE_DEVIL = "The Devil"
    """
    Enhances 1 selected card into a Gold Card
    """
    THE_TOWER = "The Tower"
    """
    Enhances 1 selected card into a Stone Card
    """
    THE_STAR = "The Star"
    """
    Converts up to 3 selected cards to Diamonds
    """
    THE_MOON = "The Moon"
    """
    Converts up to 3 selected cards to Clubs
    """
    THE_SUN = "The Sun"
    """
    Converts up to 3 selected cards to Hearts
    """
    JUDGEMENT = "Judgement"
    """
    Creates a random Joker card
    (Must have room)
    """
    THE_WORLD = "The World"
    """
    Converts up to 3 selected cards to Spades
    """

    DEFAULT = STRENGTH


class Planet(Enum):
    ERIS = "Eris"
    """
    Level up Flush Five
    +3 Mult and +50 Chips
    """
    CERES = "Ceres"
    """
    Level up Flush House
    +4 Mult and +40 Chips
    """
    PLANET_X = "Planet X"
    """
    Level up Five of a Kind
    +3 Mult and +35 Chips
    """
    NEPTUNE = "Neptune"
    """
    Level up Straight Flush
    +4 Mult and +40 Chips
    """
    MARS = "Mars"
    """
    Level up Four of a Kind
    +3 Mult and +30 Chips
    """
    EARTH = "Earth"
    """
    Level up Full House
    +2 Mult and +25 Chips
    """
    JUPITER = "Jupiter"
    """
    Level up Flush
    +2 Mult and +15 Chips
    """
    SATURN = "Saturn"
    """
    Level up Straight
    +3 Mult and +30 Chips
    """
    VENUS = "Venus"
    """
    Level up Three of a Kind
    +2 Mult and +20 Chips
    """
    URANUS = "Uranus"
    """
    Level up Two Pair
    +1 Mult and +20 Chips
    """
    MERCURY = "Mercury"
    """
    Level up Pair
    +1 Mult and +15 Chips
    """
    PLUTO = "Pluto"
    """
    Level up High Card
    +1 Mult and +10 Chips
    """

    DEFAULT = PLUTO

    @property
    def poker_hand(self) -> Planet:
        return list(PokerHand)[list(Planet).index(self)]


class Spectral(Enum):
    FAMILIAR = "Familiar"
    """
    Destroy 1 random card in your hand, add 3 random Enhanced face cards to your hand
    """
    GRIM = "Grim"
    """
    Destroy 1 random card in your hand, add 2 random Enhanced Aces to your hand
    """
    INCANTATION = "Incantation"
    """
    Destroy 1 random card in your hand, add 4 random Enhanced numbered cards to your hand
    """
    TALISMAN = "Talisman"
    """
    Add a Gold Seal to 1 selected card in your hand
    """
    AURA = "Aura"
    """
    Add Foil, Holographic, or Polychrome effect to 1 selected card in hand
    """
    WRAITH = "Wraith"
    """
    Creates a random Rare Joker, sets money to $0
    """
    SIGIL = "Sigil"
    """
    Converts all cards in hand to a single random suit
    """
    OUIJA = "Ouija"
    """
    Converts all cards in hand to a single random rank
    -1 hand size
    """
    ECTOPLASM = "Ectoplasm"
    """
    Add Negative to a random Joker,
    -1 hand size
    """
    IMMOLATE = "Immolate"
    """
    Destroys 5 random cards in hand, gain $20
    """
    ANKH = "Ankh"
    """
    Create a copy of a random Joker, destroy all other Jokers
    """
    DEJA_VU = "Deja Vu"
    """
    Add a Red Seal to 1 selected card in your hand
    """
    HEX = "Hex"
    """
    Add Polychrome to a random Joker, destroy all other Jokers
    """
    TRANCE = "Trance"
    """
    Add a Blue Seal to 1 selected card in your hand
    """
    MEDIUM = "Medium"
    """
    Add a Purple Seal to 1 selected card in your hand
    """
    CRYPTID = "Cryptid"
    """
    Create 2 copies of 1 selected card in your hand
    """
    THE_SOUL = "The Soul"
    """
    Creates a Legendary Joker
    (Must have room)
    """
    BLACK_HOLE = "Black Hole"
    """
    Upgrade every poker hand by 1 level
    """

    DEFAULT = INCANTATION


class Edition(Enum):
    BASE = "Base"
    """
    No extra effects
    """
    FOIL = "Foil"
    """
    +50 chips
    """
    HOLOGRAPHIC = "Holographic"
    """
    +10 Mult
    """
    POLYCHROME = "Polychrome"
    """
    X1.5 Mult
    """
    NEGATIVE = "Negative"
    """
    +1 Joker slot
    """


class Enhancement(Enum):
    BONUS = "Bonus"
    """
    +30 extra chips
    """
    MULT = "Mult"
    """
    +4 Mult
    """
    WILD = "Wild"
    """
    Can be used as any suit
    """
    GLASS = "Glass"
    """
    X2 Mult
    1 in 4 chance to destroy card
    """
    STEEL = "Steel"
    """
    X1.5 Mult while this card stays in hand
    """
    STONE = "Stone"
    """
    +50 Chips
    no rank or suit
    """
    GOLD = "Gold"
    """
    $3 if this card is held in hand at end of round
    """
    LUCKY = "Lucky"
    """
    1 in 5 chance for +20 Mult
    1 in 15 chance to win $20
    """


@total_ordering
class Stake(Enum):
    GOLD = "Gold"
    """
    Shop can have Rental Jokers
    (Costs $3 per round)
    Applies all previous Stakes
    """
    ORANGE = "Orange"
    """
    Shop can have Perishable Jokers
    (Debuffed after 5 Rounds)
    Applies all previous Stakes
    """
    PURPLE = "Purple"
    """
    Required score scales faster for each Ante
    Applies all previous Stakes
    """
    BLUE = "Blue"
    """
    -1 Discard
    Applies all previous Stakes
    """
    BLACK = "Black"
    """
    Shop can have Eternal Jokers
    (Can't be sold or destroyed)
    Applies all previous Stakes
    """
    GREEN = "Green"
    """
    Required score scales faster for each Ante
    Applies all previous Stakes
    """
    RED = "Red"
    """
    Small Blind gives no reward money
    Applies all previous Stakes
    """
    WHITE = "White"
    """
    Base Difficulty
    """

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
    """
    Shop has a free Uncommon Joker
    """
    RARE = "Rare Tag"
    """
    Shop has a free Rare Joker
    """
    NEGATIVE = "Negative Tag"
    """
    Next base edition shop Joker is free and becomes Negative
    """
    FOIL = "Foil Tag"
    """
    Next base edition shop Joker is free and becomes Foil
    """
    HOLOGRAPHIC = "Holographic Tag"
    """
    Next base edition shop Joker is free and becomes Holographic
    """
    POLYCHROME = "Polychrome Tag"
    """
    Next base edition shop Joker is free and becomes Polychrome
    """
    INVESTMENT = "Investment Tag"
    """
    After defeating the Boss Blind, gain $25
    """
    VOUCHER = "Voucher Tag"
    """
    Adds one Voucher to the next shop
    """
    BOSS = "Boss Tag"
    """
    Rerolls the Boss Blind
    """
    STANDARD = "Standard Tag"
    """
    Gives a free Mega Standard Pack
    """
    CHARM = "Charm Tag"
    """
    Gives a free Mega Arcana Pack
    """
    METEOR = "Meteor Tag"
    """
    Gives a free Mega Celestial Pack
    """
    BUFFOON = "Buffoon Tag"
    """
    Gives a free Mega Buffoon Pack
    """
    HANDY = "Handy Tag"
    """
    Gives $1 per played hand this run
    """
    GARBAGE = "Garbage Tag"
    """
    Gives $1 per unused discard this run
    """
    ETHEREAL = "Ethereal Tag"
    """
    Gives a free Spectral Pack
    """
    COUPON = "Coupon Tag"
    """
    Initial cards and booster packs in next shop are free
    """
    DOUBLE = "Double Tag"
    """
    Gives a copy of the next selected Tag
    Double Tag excluded
    """
    JUGGLE = "Juggle Tag"
    """
    +3 hand size next round
    """
    DSIX = "D6 Tag"
    """
    Rerolls in next shop start at $0
    """
    TOP_UP = "Top-up Tag"
    """
    Create up to 2 Common Jokers
    (Mut have room)
    """
    SPEED = "Speed Tag"
    """
    Gives $5 per skipped Blind this run
    """
    ORBITAL = "Orbital Tag"
    """
    Upgrade [poker hand] by 3 levels
    """
    ECONOMY = "Economy Tag"
    """
    Doubles your money
    (Max of $40)
    """

    def _repr_png_(self) -> bytes:
        from .sprites import get_sprite

        return get_sprite(self, as_image=False)


class Blind(Enum):
    SMALL_BLIND = "Small Blind"
    """
    Score at least 1X Base
    Reward: $$$
    """
    BIG_BLIND = "Big Blind"
    """
    Score at least 1.5X Base
    Reward: $$$$
    """
    THE_HOOK = "The Hook"
    """
    Score at least 2X Base
    Reward: $$$$$
    Discards 2 random cards per hand played
    """
    THE_OX = "The Ox"
    """
    Score at least 2X Base
    Reward: $$$$$
    Playing a [most played hand] sets money to $0
    """
    THE_HOUSE = "The House"
    """
    Score at least 2X Base
    Reward: $$$$$
    First hand is drawn face down
    """
    THE_WALL = "The Wall"
    """
    Score at least 4X Base
    Reward: $$$$$
    Extra large blind
    """
    THE_WHEEL = "The Wheel"
    """
    Score at least 2X Base
    Reward: $$$$$
    1 in 7 cards get drawn face down
    """
    THE_ARM = "The Arm"
    """
    Score at least 2X Base
    Reward: $$$$$
    Decrease level of played poker hand
    """
    THE_CLUB = "The Club"
    """
    Score at least 2X Base
    Reward: $$$$$
    All Club cards are debuffed
    """
    THE_FISH = "The Fish"
    """
    Score at least 2X Base
    Reward: $$$$$
    Cards drawn face down after each hand played
    """
    THE_PSYCHIC = "The Psychic"
    """
    Score at least 2X Base
    Reward: $$$$$
    Must play 5 cards
    """
    THE_GOAD = "The Goad"
    """
    Score at least 2X Base
    Reward: $$$$$
    All Spade cards are debuffed
    """
    THE_WATER = "The Water"
    """
    Score at least 2X Base
    Reward: $$$$$
    Start with 0 discards
    """
    THE_WINDOW = "The Window"
    """
    Score at least 2X Base
    Reward: $$$$$
    All Diamond cards are debuffed
    """
    THE_MANACLE = "The Manacle"
    """
    Score at least 2X Base
    Reward: $$$$$
    -1 Hand Size
    """
    THE_EYE = "The Eye"
    """
    Score at least 2X Base
    Reward: $$$$$
    No repeat hand types this round
    """
    THE_MOUTH = "The Mouth"
    """
    Score at least 2X Base
    Reward: $$$$$
    Play only 1 hand type this round
    """
    THE_PLANT = "The Plant"
    """
    Score at least 2X Base
    Reward: $$$$$
    All face cards are debuffed
    """
    THE_SERPENT = "The Serpent"
    """
    Score ate least 2X Base
    Reward: $$$$$
    After Play or Discard, always draw 3 cards
    """
    THE_PILLAR = "The Pillar"
    """
    Score ate least 2X Base
    Reward: $$$$$
    Cards played previously this Ante are debuffed
    """
    THE_NEEDLE = "The Needle"
    """
    Score at least 1X Base
    Reward: $$$$$
    Play only 1 hand
    """
    THE_HEAD = "The Head"
    """
    Score at least 2X Base
    Reward: $$$$$
    All Heart cards are debuffed
    """
    THE_TOOTH = "The Tooth"
    """
    Score at least 2X Base
    Reward: $$$$$
    Lose $1 per card played
    """
    THE_FLINT = "The Flint"
    """
    Score at least 2X Base
    Reward: $$$$$
    Base Chips and Mult are halved
    """
    THE_MARK = "The Mark"
    """
    Score at least 2X Base
    Reward: $$$$$
    All face cards are drawn face down
    """
    AMBER_ACORN = "Amber Acorn"
    """
    Score at least 2X Base
    Reward: $$$$$$$$
    Flips and shuffles all Joker cards
    """
    VERDANT_LEAF = "Verdant Leaf"
    """
    Score at least 2X Base
    Reward: $$$$$$$$
    All cards debuffed until 1 Joker sold
    """
    VIOLET_VESSEL = "Violet Vessel"
    """
    Score at least 6X Base
    Reward: $$$$$$$$
    Very large blind
    """
    CRIMSON_HEART = "Crimson Heart"
    """
    Score at least 2X Base
    Reward: $$$$$$$$
    One random Joker disabled every hand
    """
    CERULEAN_BELL = "Cerulean Bell"
    """
    Score at least 2X Base
    Reward: $$$$$$$$
    Forces 1 card to always be selected
    """

    def _repr_png_(self) -> bytes:
        from .sprites import get_sprite

        return get_sprite(self, as_image=False)


class Deck(Enum):
    RED = "Red"
    """
    +1 discard every round
    """
    BLUE = "Blue"
    """
    +1 hand every round
    """
    YELLOW = "Yellow"
    """
    Start with extra $10
    """
    GREEN = "Green"
    """
    At end of each Round:
    $2 per remaining Hand
    $1 per remaining Discard
    Earn no Interest
    """
    BLACK = "Black"
    """
    +1 Joker slot
    -1 hand every round
    """
    MAGIC = "Magic"
    """
    Start run with the Crystal Ball voucher and 2 copies of The Fool
    """
    NEBULA = "Nebula"
    """
    Start run with the Telescope voucher
    -1 consumable slot
    """
    GHOST = "Ghost"
    """
    Spectral cards may appear in the shop,
    start with a Hex card
    """
    ABANDONED = "Abandoned"
    """
    Start run with no Face Cards in your deck
    """
    CHECKERED = "Checkered"
    """
    Start run with 26 Spades and 26 Hearts in deck
    """
    ZODIAC = "Zodiac"
    """
    Start run with Tarot Merchant, Planet Merchant, and Overstock
    """
    PAINTED = "Painted"
    """
    +2 hand size,
    -1 Joker slot
    """
    ANAGLYPH = "Anaglyph"
    """
    After defeating each Boss Blind, gain a Double Tag
    """
    PLASMA = "Plasma"
    """
    Balance Chips and Mult when calculating score for played hand
    X2 base Blind size
    """
    ERRATIC = "Erratic"
    """
    All Rank and Suits in deck are randomized
    """

    CHALLENGE = "Challenge"

    def _repr_png_(self) -> bytes:
        from .sprites import get_sprite

        return get_sprite(self, as_image=False)

    @property
    def starting_size(self) -> int:
        return 40 if self is Deck.ABANDONED else 52


class Seal(Enum):
    GOLD = "Gold"
    """
    Earn $3 when this card is played and scores
    """
    RED = "Red"
    """
    Retrigger this card 1 time
    """
    BLUE = "Blue"
    """
    Creates the Planet card for final played poker hand of round if held in hand
    (Must have room)
    """
    PURPLE = "Purple"
    """
    Creates a Tarot card when discarded
    (Must have room)
    """


class Pack(Enum):
    ARCANA = "Arcana Pack"
    """
    Choose 1 of up to 3 Tarot cards to be used immediately
    """
    JUMBO_ARCANA = "Jumbo Arcana Pack"
    """
    Choose 1 of up to 5 Tarot cards to be used immediately
    """
    MEGA_ARCANA = "Mega Arcana Pack"
    """
    Choose 2 of up to 5 Tarot cards to be used immediately
    """
    CELESTIAL = "Celestial Pack"
    """
    Choose 1 of up to 3 Planet cards to be used immediately
    """
    JUMBO_CELESTIAL = "Jumbo Celestial Pack"
    """
    Choose 1 of up to 5 Planet cards to be used immediately
    """
    MEGA_CELESTIAL = "Mega Celestial Pack"
    """
    Choose 2 of up to 5 Planet cards to be used immediately
    """
    SPECTRAL = "Spectral Pack"
    """
    Choose 1 of up to 2 Spectral cards to be used immediately
    """
    JUMBO_SPECTRAL = "Jumbo Spectral Pack"
    """
    Choose 1 of up to 4 Spectral cards to be used immediately
    """
    MEGA_SPECTRAL = "Mega Spectral Pack"
    """
    Choose 2 of up to 4 Spectral cards to be used immediately
    """
    STANDARD = "Standard Pack"
    """
    Choose 1 of up to 3 Playing cards to add to your deck
    """
    JUMBO_STANDARD = "Jumbo Standard Pack"
    """
    Choose 1 of up to 5 Playing cards to add to your deck
    """
    MEGA_STANDARD = "Mega Standard Pack"
    """
    Choose 2 of up to 5 Playing cards to add to your deck
    """
    BUFFOON = "Buffoon Pack"
    """
    Choose 1 of up to 2 Joker cards
    """
    JUMBO_BUFFOON = "Jumbo Buffoon Pack"
    """
    Choose 1 of up to 4 Joker cards
    """
    MEGA_BUFFOON = "Mega Buffoon Pack"
    """
    Choose 2 of up to 4 Joker cards
    """

    def _repr_png_(self) -> bytes:
        from .sprites import get_sprite

        return get_sprite(self, as_image=False)


class Suit(Enum):
    SPADES = "Spades"
    HEARTS = "Hearts"
    CLUBS = "Clubs"
    DIAMONDS = "Diamonds"


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
    """
    5 cards with the same rank and suit
    """
    FLUSH_HOUSE = "Flush House"
    """
    A Three of a Kind and a Pair with all cards sharing the same suit
    """
    FIVE_OF_A_KIND = "Five of a Kind"
    """
    5 cards with the same rank
    """
    STRAIGHT_FLUSH = "Straight Flush"
    """
    5 cards in a row (consecutive ranks) with all cards sharing the same suit
    """
    FOUR_OF_A_KIND = "Four of a Kind"
    """
    4 cards with the same rank. THey may be played with 1 other unscored card
    """
    FULL_HOUSE = "Full House"
    """
    A Three of a Kind and a Pair
    """
    FLUSH = "Flush"
    """
    5 cards that share the same suit
    """
    STRAIGHT = "Straight"
    """
    5 cards in a row (consecutive ranks)
    """
    THREE_OF_A_KIND = "Three of a Kind"
    """
    3 cards with the same rank. They may be played with up to 2 other unscored cards
    """
    TWO_PAIR = "Two Pair"
    """
    2 pairs of cards with different ranks, may be played with 1 other unscored card
    """
    PAIR = "Pair"
    """
    2 cards that share the same rank. They may be played with up to 3 other unscored cards
    """
    HIGH_CARD = "High Card"
    """
    If the played hand is not any of the above hands, only the highest ranked card scores
    """

    def __lt__(self, other: PokerHand) -> bool:
        match other:
            case PokerHand():
                return list(PokerHand).index(self) > list(PokerHand).index(other)

        return NotImplemented

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
