from balatro_enums import *
from balatro_jokers import *

JOKER_TYPE_RARITIES = {
    Rarity.COMMON: list(JokerType)[:61],
    Rarity.UNCOMMON: list(JokerType)[61 : 61 + 64],
    Rarity.RARE: list(JokerType)[61 + 64 : 61 + 64 + 20],
    Rarity.LEGENDARY: list(JokerType)[61 + 64 + 20 : 61 + 64 + 20 + 5],
}

# NON_COPYABLE_JOKERS = {
#     JokerType.CREDIT_CARD,  #
#     JokerType.CHAOS,  #
#     JokerType.DELAYED_GRAT,  #
#     JokerType.EGG,  #
#     JokerType.SPLASH,  #
#     JokerType.JUGGLER,  #
#     JokerType.DRUNKARD,  #
#     JokerType.GOLDEN,  #
#     JokerType.FOUR_FINGERS,  #
#     JokerType.PAREIDOLIA,  #
#     JokerType.SIXTH_SENSE,  #
#     JokerType.SHORTCUT,  #
#     JokerType.CLOUD_9,  #
#     JokerType.ROCKET,  #
#     JokerType.MIDAS_MASK,  #
#     JokerType.GIFT,  #
#     JokerType.TURTLE_BEAN,  #
#     JokerType.TO_THE_MOON,  #
#     JokerType.TRADING,  #
#     JokerType.MR_BONES,  #
#     JokerType.TROUBADOUR,  #
#     JokerType.SMEARED,  #
#     JokerType.RING_MASTER,  #
#     JokerType.MERRY_ANDY,  #
#     JokerType.OOPS,  #
#     JokerType.SATELLITE,  #
#     JokerType.ASTRONOMER,  #
#     JokerType.INVISIBLE,  #
#     JokerType.CHICOT,  #
# }

JOKER_CLASSES = {
    JokerType.BLUEPRINT: Blueprint,
    JokerType.BRAINSTORM: Brainstorm,
    JokerType.SPACE: SpaceJoker,
    JokerType.DNA: DNA,
    JokerType.TODO_LIST: ToDoList,
    JokerType.MIDAS_MASK: MidasMask,
    JokerType.GREEDY_JOKER: GreedyJoker,
    JokerType.LUSTY_JOKER: LustyJoker,
    JokerType.WRATHFUL_JOKER: WrathfulJoker,
    JokerType.GLUTTENOUS_JOKER: GluttonousJoker,
    JokerType.EIGHT_BALL: EightBall,
    JokerType.DUSK: Dusk,
    JokerType.FIBONACCI: Fibonacci,
    JokerType.SCARY_FACE: ScaryFace,
    JokerType.HACK: Hack,
    JokerType.EVEN_STEVEN: EvenSteven,
    JokerType.ODD_TODD: OddTodd,
    JokerType.SCHOLAR: Scholar,
    JokerType.BUSINESS: BusinessCard,
    JokerType.HIKER: Hiker,
    JokerType.PHOTOGRAPH: Photograph,
    JokerType.ANCIENT: AncientJoker,
    JokerType.WALKIE_TALKIE: WalkieTalkie,
    JokerType.SELTZER: Seltzer,
    JokerType.SMILEY: SmileyFace,
    JokerType.TICKET: GoldenTicket,
    JokerType.SOCK_AND_BUSKIN: SockAndBuskin,
    JokerType.HANGING_CHAD: HangingChad,
    JokerType.ROUGH_GEM: RoughGem,
    JokerType.BLOODSTONE: Bloodstone,
    JokerType.ARROWHEAD: Arrowhead,
    JokerType.ONYX_AGATE: OnyxAgate,
    JokerType.IDOL: TheIdol,
    JokerType.TRIBOULET: Triboulet,
    JokerType.MIME: Mime,
    JokerType.RAISED_FIST: RaisedFist,
    JokerType.BARON: Baron,
    JokerType.RESERVED_PARKING: ReservedParking,
    JokerType.SHOOT_THE_MOON: ShootTheMoon,
    JokerType.JOKER: Jimbo,
    JokerType.JOLLY: JollyJoker,
    JokerType.ZANY: ZanyJoker,
    JokerType.MAD: MadJoker,
    JokerType.CRAZY: CrazyJoker,
    JokerType.DROLL: DrollJoker,
    JokerType.SLY: SlyJoker,
    JokerType.WILY: WilyJoker,
    JokerType.CLEVER: CleverJoker,
    JokerType.DEVIOUS: DeviousJoker,
    JokerType.CRAFTY: CraftyJoker,
    JokerType.HALF: HalfJoker,
    JokerType.STENCIL: JokerStencil,
    JokerType.CEREMONIAL: CeremonialDagger,
    JokerType.BANNER: Banner,
    JokerType.MYSTIC_SUMMIT: MysticSummit,
    JokerType.LOYALTY_CARD: LoyaltyCard,
    JokerType.MISPRINT: Misprint,
    JokerType.STEEL_JOKER: SteelJoker,
    JokerType.ABSTRACT: AbstractJoker,
    JokerType.GROS_MICHEL: GrosMichel,
    JokerType.SUPERNOVA: Supernova,
    JokerType.BLACKBOARD: Blackboard,
    JokerType.ICE_CREAM: IceCream,
    JokerType.BLUE_JOKER: BlueJoker,
    JokerType.CONSTELLATION: Constellation,
    JokerType.SUPERPOSITION: Superposition,
    JokerType.CAVENDISH: Cavendish,
    JokerType.CARD_SHARP: CardSharp,
    JokerType.RED_CARD: RedCard,
    JokerType.MADNESS: Madness,
    JokerType.SEANCE: Seance,
    JokerType.HOLOGRAM: Hologram,
    JokerType.VAGABOND: Vagabond,
    JokerType.EROSION: Erosion,
    JokerType.FORTUNE_TELLER: FortuneTeller,
    JokerType.STONE: StoneJoker,
    JokerType.BULL: Bull,
    JokerType.FLASH: FlashCard,
    JokerType.POPCORN: Popcorn,
    JokerType.CAMPFIRE: Campfire,
    JokerType.ACROBAT: Acrobat,
    JokerType.SWASHBUCKLER: Swashbuckler,
    JokerType.THROWBACK: Throwback,
    JokerType.GLASS: GlassJoker,
    JokerType.FLOWER_POT: FlowerPot,
    JokerType.SEEING_DOUBLE: SeeingDouble,
    JokerType.MATADOR: Matador,
    JokerType.DUO: TheDuo,
    JokerType.TRIO: TheTrio,
    JokerType.FAMILY: TheFamily,
    JokerType.ORDER: TheOrder,
    JokerType.TRIBE: TheTribe,
    JokerType.STUNTMAN: Stuntman,
    JokerType.DRIVERS_LICENSE: DriversLicense,
    JokerType.BOOTSTRAPS: Bootstraps,
    JokerType.CANIO: Canio,
    JokerType.RIDE_THE_BUS: RideTheBus,
    JokerType.RUNNER: Runner,
    JokerType.GREEN_JOKER: GreenJoker,
    JokerType.SQUARE: SquareJoker,
    JokerType.VAMPIRE: Vampire,
    JokerType.OBELISK: Obelisk,
    JokerType.LUCKY_CAT: LuckyCat,
    JokerType.TROUSERS: SpareTrousers,
    JokerType.RAMEN: Ramen,
    JokerType.CASTLE: Castle,
    JokerType.WEE: WeeJoker,
    JokerType.HIT_THE_ROAD: HitTheRoad,
    JokerType.YORICK: Yorick,
    JokerType.BASEBALL: BaseballCard,
    JokerType.FACELESS: FacelessJoker,
    JokerType.MAIL: MailInRebate,
    JokerType.TRADING: TradingCard,
    JokerType.BURNT: BurntJoker,
    JokerType.FOUR_FINGERS: FourFingers,
    JokerType.CREDIT_CARD: CreditCard,
    JokerType.MARBLE: MarbleJoker,
    JokerType.CHAOS: ChaosTheClown,
    JokerType.DELAYED_GRAT: DelayedGratification,
    JokerType.PAREIDOLIA: Pareidolia,
    JokerType.EGG: Egg,
    JokerType.BURGLAR: Burglar,
    JokerType.SPLASH: Splash,
    JokerType.SIXTH_SENSE: SixthSense,
    JokerType.RIFF_RAFF: RiffRaff,
    JokerType.SHORTCUT: Shortcut,
    JokerType.CLOUD_9: CloudNine,
    JokerType.ROCKET: Rocket,
    JokerType.LUCHADOR: Luchador,
    JokerType.GIFT: GiftCard,
    JokerType.TURTLE_BEAN: TurtleBean,
    JokerType.TO_THE_MOON: ToTheMoon,
    JokerType.HALLUCINATION: Hallucination,
    JokerType.JUGGLER: Juggler,
    JokerType.DRUNKARD: Drunkard,
    JokerType.GOLDEN: GoldenJoker,
    JokerType.DIET_COLA: DietCola,
    JokerType.MR_BONES: MrBones,
    JokerType.TROUBADOUR: Troubadour,
    JokerType.CERTIFICATE: Certificate,
    JokerType.SMEARED: SmearedJoker,
    JokerType.RING_MASTER: Showman,
    JokerType.MERRY_ANDY: MerryAndy,
    JokerType.OOPS: OopsAllSixes,
    JokerType.INVISIBLE: InvisibleJoker,
    JokerType.SATELLITE: Satellite,
    JokerType.CARTOMANCER: Cartomancer,
    JokerType.ASTRONOMER: Astronomer,
    JokerType.CHICOT: Chicot,
    JokerType.PERKEO: Perkeo,
}
