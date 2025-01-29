from __future__ import annotations
import colorsys
import io
import math
from PIL import Image, ImageFilter, ImageEnhance, ImageDraw
import numpy as np
import base64
import random as r

from .classes import *
from .enums import *
from .jokers import *

DEFAULT_CARD_WIDTH, DEFAULT_CARD_HEIGHT = 142, 190
DEFAULT_CHIP_WIDTH, DEFAULT_CHIP_HEIGHT = 58, 58
DEFAULT_TAG_WIDTH, DEFAULT_TAG_HEIGHT = 68, 68
DEFAULT_BLIND_WIDTH, DEFAULT_BLIND_HEIGHT = 68, 68

BLIND_ROWS = {
    Blind.SMALL_BLIND: 0,
    Blind.BIG_BLIND: 1,
    Blind.THE_OX: 2,
    Blind.THE_HOUSE: 3,
    Blind.THE_CLUB: 4,
    Blind.THE_FISH: 5,
    Blind.THE_WINDOW: 6,
    Blind.THE_HOOK: 7,
    Blind.THE_MANACLE: 8,
    Blind.THE_WALL: 9,
    Blind.THE_WHEEL: 10,
    Blind.THE_ARM: 11,
    Blind.THE_PSYCHIC: 12,
    Blind.THE_GOAD: 13,
    Blind.THE_WATER: 14,
    Blind.THE_SERPENT: 15,
    Blind.THE_PILLAR: 16,
    Blind.THE_EYE: 17,
    Blind.THE_MOUTH: 18,
    Blind.THE_PLANT: 19,
    Blind.THE_NEEDLE: 20,
    Blind.THE_HEAD: 21,
    Blind.THE_TOOTH: 22,
    Blind.THE_MARK: 23,
    Blind.THE_FLINT: 24,
    Blind.CRIMSON_HEART: 25,
    Blind.CERULEAN_BELL: 26,
    Blind.AMBER_ACORN: 27,
    Blind.VERDANT_LEAF: 28,
    Blind.VIOLET_VESSEL: 29,
}
CHIPS_COORDINATES = {
    Stake.WHITE: [0, 0],
    Stake.RED: [0, 1],
    Stake.GREEN: [0, 2],
    Stake.BLUE: [0, 3],
    Stake.BLACK: [0, 4],
    Stake.PURPLE: [1, 0],
    Stake.ORANGE: [1, 1],
    Stake.GOLD: [1, 3],
}
CONSUMABLE_COORDINATES = {
    Tarot.THE_FOOL: [0, 0],
    Tarot.THE_MAGICIAN: [0, 1],
    Tarot.THE_HIGH_PRIESTESS: [0, 2],
    Tarot.THE_EMPRESS: [0, 3],
    Tarot.THE_EMPEROR: [0, 4],
    Tarot.THE_HEIROPHANT: [0, 5],
    Tarot.THE_LOVERS: [0, 6],
    Tarot.THE_CHARIOT: [0, 7],
    Tarot.JUSTICE: [0, 8],
    Tarot.THE_HERMIT: [0, 9],
    Tarot.THE_WHEEL_OF_FORTUNE: [1, 0],
    Tarot.STRENGTH: [1, 1],
    Tarot.THE_HANGED_MAN: [1, 2],
    Tarot.DEATH: [1, 3],
    Tarot.TEMPERANCE: [1, 4],
    Tarot.THE_DEVIL: [1, 5],
    Tarot.THE_TOWER: [1, 6],
    Tarot.THE_STAR: [1, 7],
    Tarot.THE_MOON: [1, 8],
    Tarot.THE_SUN: [1, 9],
    Tarot.JUDGEMENT: [2, 0],
    Tarot.THE_WORLD: [2, 1],
    Planet.ERIS: [2, 3],
    Planet.CERES: [2, 8],
    Planet.PLANET_X: [2, 9],
    Planet.MERCURY: [3, 0],
    Planet.VENUS: [3, 1],
    Planet.EARTH: [3, 2],
    Planet.MARS: [3, 3],
    Planet.JUPITER: [3, 4],
    Planet.SATURN: [3, 5],
    Planet.URANUS: [3, 6],
    Planet.NEPTUNE: [3, 7],
    Planet.PLUTO: [3, 8],
    Spectral.THE_SOUL: [2, 2],
    Spectral.BLACK_HOLE: [3, 9],
    Spectral.FAMILIAR: [4, 0],
    Spectral.GRIM: [4, 1],
    Spectral.INCANTATION: [4, 2],
    Spectral.TALISMAN: [4, 3],
    Spectral.AURA: [4, 4],
    Spectral.WRAITH: [4, 5],
    Spectral.SIGIL: [4, 6],
    Spectral.OUIJA: [4, 7],
    Spectral.ECTOPLASM: [4, 8],
    Spectral.IMMOLATE: [4, 9],
    Spectral.ANKH: [5, 0],
    Spectral.DEJA_VU: [5, 1],
    Spectral.HEX: [5, 2],
    Spectral.TRANCE: [5, 3],
    Spectral.MEDIUM: [5, 4],
    Spectral.CRYPTID: [5, 5],
}
ENHANCER_COORDINATES = {
    Deck.RED: [0, 0],
    Seal.GOLD: [0, 2],
    Deck.NEBULA: [0, 3],
    Enhancement.STONE: [0, 5],
    Enhancement.GOLD: [0, 6],
    Enhancement.BONUS: [1, 1],
    Enhancement.MULT: [1, 2],
    Enhancement.WILD: [1, 3],
    Enhancement.LUCKY: [1, 4],
    Enhancement.GLASS: [1, 5],
    Enhancement.STEEL: [1, 6],
    Deck.BLUE: [2, 0],
    Deck.YELLOW: [2, 1],
    Deck.GREEN: [2, 2],
    Deck.BLACK: [2, 3],
    Deck.PLASMA: [2, 4],
    Deck.GHOST: [2, 6],
    Deck.MAGIC: [3, 0],
    Deck.CHECKERED: [3, 1],
    Deck.ERRATIC: [3, 2],
    Deck.ABANDONED: [3, 3],
    Deck.PAINTED: [3, 4],
    Deck.CHALLENGE: [4, 0],
    Deck.ANAGLYPH: [4, 2],
    Deck.ZODIAC: [4, 3],
    Seal.PURPLE: [4, 4],
    Seal.RED: [4, 5],
    Seal.BLUE: [4, 6],
}
JOKER_COORDINATES = {
    Joker: [0, 0],
    ChaosTheClown: [0, 1],
    JollyJoker: [0, 2],
    ZanyJoker: [0, 3],
    MadJoker: [0, 4],
    CrazyJoker: [0, 5],
    DrollJoker: [0, 6],
    HalfJoker: [0, 7],
    MerryAndy: [0, 8],
    StoneJoker: [0, 9],
    Juggler: [1, 0],
    Drunkard: [1, 1],
    Acrobat: [1, 2],
    SockAndBuskin: [1, 3],
    Mime: [1, 4],
    CreditCard: [1, 5],
    GreedyJoker: [1, 6],
    LustyJoker: [1, 7],
    WrathfulJoker: [1, 8],
    GluttonousJoker: [1, 9],
    Troubadour: [2, 0],
    Banner: [2, 1],
    MysticSummit: [2, 2],
    MarbleJoker: [2, 3],
    LoyaltyCard: [2, 4],
    Hack: [2, 5],
    Misprint: [2, 6],
    SteelJoker: [2, 7],
    RaisedFist: [2, 8],
    GoldenJoker: [2, 9],
    Blueprint: [3, 0],
    GlassJoker: [3, 1],
    ScaryFace: [3, 2],
    AbstractJoker: [3, 3],
    DelayedGratification: [3, 4],
    GoldenTicket: [3, 5],
    Pareidolia: [3, 6],
    Cartomancer: [3, 7],
    EvenSteven: [3, 8],
    OddTodd: [3, 9],
    Scholar: [4, 0],
    BusinessCard: [4, 1],
    Supernova: [4, 2],
    MrBones: [4, 3],
    SeeingDouble: [4, 4],
    TheDuo: [4, 5],
    TheTrio: [4, 6],
    TheFamily: [4, 7],
    TheOrder: [4, 8],
    TheTribe: [4, 9],
    EightBall: [5, 0],
    Fibonacci: [5, 1],
    JokerStencil: [5, 2],
    SpaceJoker: [5, 3],
    Matador: [5, 4],
    CeremonialDagger: [5, 5],
    Showman: [5, 6],
    FortuneTeller: [5, 7],
    HitTheRoad: [5, 8],
    Swashbuckler: [5, 9],
    FlowerPot: [6, 0],
    RideTheBus: [6, 1],
    ShootTheMoon: [6, 2],
    SmearedJoker: [6, 4],
    OopsAllSixes: [6, 5],
    FourFingers: [6, 6],
    GrosMichel: [6, 7],
    Stuntman: [6, 8],
    HangingChad: [6, 9],
    DriversLicense: [7, 0],
    InvisibleJoker: [7, 1],
    Astronomer: [7, 2],
    BurntJoker: [7, 3],
    Dusk: [7, 4],
    Throwback: [7, 5],
    TheIdol: [7, 6],
    Brainstorm: [7, 7],
    Satellite: [7, 8],
    RoughGem: [7, 9],
    Bloodstone: [8, 0],
    Arrowhead: [8, 1],
    OnyxAgate: [8, 2],
    Canio: [8, 3],
    Triboulet: [8, 4],
    Yorick: [8, 5],
    Chicot: [8, 6],
    Perkeo: [8, 7],
    Certificate: [8, 8],
    Bootstraps: [8, 9],
    Egg: [10, 0],
    Burglar: [10, 1],
    Blackboard: [10, 2],
    Runner: [10, 3],
    IceCream: [10, 4],
    DNA: [10, 5],
    Splash: [10, 6],
    BlueJoker: [10, 7],
    SixthSense: [10, 8],
    Constellation: [10, 9],
    Hiker: [11, 0],
    FacelessJoker: [11, 1],
    GreenJoker: [11, 2],
    Superposition: [11, 3],
    ToDoList: [11, 4],
    Cavendish: [11, 5],
    CardSharp: [11, 6],
    RedCard: [11, 7],
    Madness: [11, 8],
    SquareJoker: [11, 9],
    Seance: [12, 0],
    RiffRaff: [12, 1],
    Vampire: [12, 2],
    Shortcut: [12, 3],
    Hologram: [12, 4],
    Vagabond: [12, 5],
    Baron: [12, 6],
    CloudNine: [12, 7],
    Rocket: [12, 8],
    Obelisk: [12, 9],
    MidasMask: [13, 0],
    Luchador: [13, 1],
    Photograph: [13, 2],
    GiftCard: [13, 3],
    TurtleBean: [13, 4],
    Erosion: [13, 5],
    ReservedParking: [13, 6],
    MailInRebate: [13, 7],
    ToTheMoon: [13, 8],
    Hallucination: [13, 9],
    SlyJoker: [14, 0],
    WilyJoker: [14, 1],
    CleverJoker: [14, 2],
    DeviousJoker: [14, 3],
    CraftyJoker: [14, 4],
    LuckyCat: [14, 5],
    BaseballCard: [14, 6],
    Bull: [14, 7],
    DietCola: [14, 8],
    TradingCard: [14, 9],
    FlashCard: [15, 0],
    Popcorn: [15, 1],
    Ramen: [15, 2],
    Seltzer: [15, 3],
    SpareTrousers: [15, 4],
    Campfire: [15, 5],
    SmileyFace: [15, 6],
    AncientJoker: [15, 7],
    WalkieTalkie: [15, 8],
    Castle: [15, 9],
}
PACK_COORDINATES = {
    Pack.ARCANA: [[0, 0], [0, 1], [0, 2], [0, 3]],
    Pack.CELESTIAL: [[1, 0], [1, 1], [1, 2], [1, 3]],
    Pack.JUMBO_ARCANA: [[2, 0], [2, 1]],
    Pack.MEGA_ARCANA: [[2, 2], [2, 3]],
    Pack.JUMBO_CELESTIAL: [[3, 0], [3, 1]],
    Pack.MEGA_CELESTIAL: [[3, 2], [3, 3]],
    Pack.SPECTRAL: [[4, 0], [4, 1]],
    Pack.JUMBO_SPECTRAL: [[4, 2]],
    Pack.MEGA_SPECTRAL: [[4, 3]],
    Pack.STANDARD: [[6, 0], [6, 1], [6, 2], [6, 3]],
    Pack.JUMBO_STANDARD: [[7, 0], [7, 1]],
    Pack.MEGA_STANDARD: [[7, 2], [7, 3]],
    Pack.BUFFOON: [[8, 0], [8, 1]],
    Pack.JUMBO_BUFFOON: [[8, 2]],
    Pack.MEGA_BUFFOON: [[8, 3]],
}
RANK_COLUMNS = {rank: i for i, rank in enumerate(reversed(Rank))}
SUIT_ROWS = {Suit.HEARTS: 0, Suit.CLUBS: 1, Suit.DIAMONDS: 2, Suit.SPADES: 3}
TAG_COORDINATES = {
    Tag.UNCOMMON: [0, 0],
    Tag.RARE: [0, 1],
    Tag.NEGATIVE: [0, 2],
    Tag.FOIL: [0, 3],
    Tag.COUPON: [0, 4],
    Tag.DOUBLE: [0, 5],
    Tag.HOLOGRAPHIC: [1, 0],
    Tag.POLYCHROME: [1, 1],
    Tag.INVESTMENT: [1, 2],
    Tag.VOUCHER: [1, 3],
    Tag.TOP_UP: [1, 4],
    Tag.JUGGLE: [1, 5],
    Tag.BOSS: [2, 0],
    Tag.STANDARD: [2, 1],
    Tag.CHARM: [2, 2],
    Tag.METEOR: [2, 3],
    Tag.BUFFOON: [2, 4],
    Tag.ORBITAL: [2, 5],
    Tag.SPEED: [3, 0],
    Tag.HANDY: [3, 1],
    Tag.GARBAGE: [3, 2],
    Tag.ETHEREAL: [3, 3],
    Tag.ECONOMY: [3, 4],
    Tag.DSIX: [3, 5],
}
VOUCHER_COORDINATES = {
    Voucher.OVERSTOCK: [0, 0],
    Voucher.TAROT_MERCHANT: [0, 1],
    Voucher.PLANET_MERCHANT: [0, 2],
    Voucher.CLEARANCE_SALE: [0, 3],
    Voucher.HONE: [0, 4],
    Voucher.GRABBER: [0, 5],
    Voucher.WASTEFUL: [0, 6],
    Voucher.BLANK: [0, 7],
    Voucher.OVERSTOCK_PLUS: [1, 0],
    Voucher.TAROT_TYCOON: [1, 1],
    Voucher.PLANET_TYCOON: [1, 2],
    Voucher.LIQUIDATION: [1, 3],
    Voucher.GLOW_UP: [1, 4],
    Voucher.NACHO_TONG: [1, 5],
    Voucher.RECYCLOMANCY: [1, 6],
    Voucher.ANTIMATTER: [1, 7],
    Voucher.REROLL_SURPLUS: [2, 0],
    Voucher.SEED_MONEY: [2, 1],
    Voucher.CRYSTAL_BALL: [2, 2],
    Voucher.TELESCOPE: [2, 3],
    Voucher.MAGIC_TRICK: [2, 4],
    Voucher.HIEROGLYPH: [2, 5],
    Voucher.DIRECTORS_CUT: [2, 6],
    Voucher.PAINT_BRUSH: [2, 7],
    Voucher.REROLL_GLUT: [3, 0],
    Voucher.MONEY_TREE: [3, 1],
    Voucher.OMEN_GLOBE: [3, 2],
    Voucher.OBSERVATORY: [3, 3],
    Voucher.ILLUSION: [3, 4],
    Voucher.PETROGLYPH: [3, 5],
    Voucher.RETCON: [3, 6],
    Voucher.PALETTE: [3, 7],
}

with io.BytesIO() as buffer:
    with open("resources/textures/ShopSignAnimation.txt") as file:
        sprite = Image.open(io.BytesIO(base64.b64decode(file.read()))).crop(
            (0, 0, 226, 114)
        )
        sprite.save(buffer, "png")
        SHOP_SIGN = buffer.getvalue()


def _apply_debuff(image: Image.Image) -> Image.Image:
    # Convert image to numpy array for processing
    img_array = np.array(image).astype(float) / 255.0

    # Get image dimensions
    height, width = img_array.shape[:2]

    # Create coordinate matrices for the X pattern
    y, x = np.indices((height, width))

    # Normalize coordinates to 0-1 range
    x = x / width
    y = y / height

    # Create the X pattern
    # The pattern is created when x+y or (1-x)+y is close to 1
    width_of_line = 0.1
    x_pattern1 = np.abs(x + y - 1.0) < width_of_line
    x_pattern2 = np.abs((1.0 - x) + y - 1.0) < width_of_line
    x_pattern = x_pattern1 | x_pattern2

    # Process each pixel
    result = np.zeros_like(img_array)
    for i in range(height):
        for j in range(width):
            r, g, b = img_array[i, j, :3]
            if img_array[i, j, 3] < 0.01:  # Skip fully transparent pixels
                result[i, j] = img_array[i, j]
                continue

            # Convert to HLS (similar to shader's HSL conversion)
            h, l, s = colorsys.rgb_to_hls(r, g, b)

            if x_pattern[i, j]:
                # Enhance red for the X pattern
                h = 1.0  # Red hue
                s = 1
                l = l * 0.8
                a = img_array[i, j, 3]  # Keep original alpha

            # s = 0.7

            # Convert back to RGB
            r, g, b = colorsys.hls_to_rgb(h, l, s)
            result[i, j] = [r, g, b, a]

    # Convert back to PIL Image
    result = (result * 255).astype(np.uint8)
    img = Image.fromarray(result)
    conv = ImageEnhance.Color(img)
    return conv.enhance(0.7)


def _apply_edition(sprite: Image.Image, edition: Edition) -> Image.Image:
    match edition:
        case Edition.BASE:
            return sprite
        case Edition.FOIL:
            return _apply_foil(sprite)
        case Edition.HOLOGRAPHIC:
            return _apply_holo(sprite)
        case Edition.POLYCHROME:
            return _apply_polychrome(sprite)
        case Edition.NEGATIVE:
            return _apply_negative(sprite)


def _apply_foil(sprite: Image.Image) -> Image.Image:
    width, height = sprite.size
    aspect_ratio = height / width
    texture_details = (0, 0, width, height)
    image_details = (width, height)
    foil = (0, 0)

    foil_overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    foil_pixels = foil_overlay.load()
    base_pixels = sprite.load()

    for x in range(width):
        for y in range(height):
            texture_coords = (x / width, y / height)
            uv_x = (
                texture_coords[0] * image_details[0]
                - texture_details[0] * texture_details[2]
            ) / texture_details[2]
            uv_y = (
                texture_coords[1] * image_details[1]
                - texture_details[1] * texture_details[3]
            ) / texture_details[3]
            uv = (uv_x, uv_y)

            adjusted_uv_x = uv[0] - 0.5
            adjusted_uv_y = uv[1] - 0.5
            adjusted_uv = (adjusted_uv_x, adjusted_uv_y)

            r, g, b, a = base_pixels[x, y]
            if a == 0:
                continue
            tex_r, tex_g, tex_b = r / 255.0, g / 255.0, b / 255.0

            low = min(tex_r, min(tex_g, tex_b))
            high = max(tex_r, max(tex_g, tex_b))
            delta = min(high, max(0.5, 1.0 - low))

            scaled_adjusted_uv_y = adjusted_uv_y * aspect_ratio
            ripple_factor = math.sqrt(adjusted_uv_x**2 + scaled_adjusted_uv_y**2)

            fac = max(
                min(
                    2.0
                    * math.sin(
                        (90.0 * ripple_factor + foil[0] * 2.0)
                        + 3.0
                        * (
                            1.0
                            + 0.8 * math.cos(113.1121 * ripple_factor - foil[0] * 3.121)
                        )
                    )
                    - 1.0
                    - max(5.0 - 90.0 * ripple_factor, 0.0),
                    1.0,
                ),
                0.0,
            )

            rotater = (math.cos(foil[0] * 0.1221), math.sin(foil[0] * 0.3512))
            angle = (
                (rotater[0] * adjusted_uv[0] + rotater[1] * adjusted_uv[1])
                / (
                    math.sqrt(rotater[0] ** 2 + rotater[1] ** 2)
                    * math.sqrt(adjusted_uv[0] ** 2 + adjusted_uv[1] ** 2)
                )
                if (rotater[0] ** 2 + rotater[1] ** 2) > 0
                and (adjusted_uv[0] ** 2 + adjusted_uv[1] ** 2) > 0
                else 0
            )
            fac2 = max(
                min(
                    5.0
                    * math.cos(
                        foil[1] * 0.3
                        + angle
                        * 3.14
                        * (2.2 + 0.9 * math.sin(foil[0] * 1.65 + 0.2 * foil[1]))
                    )
                    - 4.0
                    - max(
                        2.0
                        - 20.0 * math.sqrt(adjusted_uv[0] ** 2 + adjusted_uv[1] ** 2),
                        0.0,
                    ),
                    1.0,
                ),
                0.0,
            )
            fac3 = 0.3 * max(
                min(
                    2.0
                    * math.sin(
                        foil[0] * 5.0
                        + uv[0] * 3.0
                        + 3.0 * (1.0 + 0.5 * math.cos(foil[0] * 7.0))
                    )
                    - 1.0,
                    1.0,
                ),
                -1.0,
            )
            fac4 = 0.3 * max(
                min(
                    2.0
                    * math.sin(
                        foil[0] * 6.66
                        + uv[1] * 3.8
                        + 3.0 * (1.0 + 0.5 * math.cos(foil[0] * 3.414))
                    )
                    - 1.0,
                    1.0,
                ),
                -1.0,
            )

            maxfac = max(
                max(fac, max(fac2, max(fac3, max(fac4, 0.0))))
                + 2.2 * (fac + fac2 + fac3 + fac4),
                0.0,
            )

            foil_r = tex_r - delta + delta * maxfac * 0.3
            foil_g = tex_g - delta + delta * maxfac * 0.3
            foil_b = tex_b + delta * maxfac * 1.9
            foil_alpha = min(1.0, 0.5 * 1.0 + 0.8 * min(0.7, maxfac * 0.2))

            final_foil_alpha = foil_alpha * (a / 255.0)

            foil_pixels[x, y] = (
                int(max(0, min(1, foil_r)) * 255),
                int(max(0, min(1, foil_g)) * 255),
                int(max(0, min(1, foil_b)) * 255),
                int(max(0, min(1, foil_alpha - 0.1)) * 255),
            )

    return Image.alpha_composite(sprite, foil_overlay)


def _apply_holo(sprite: Image.Image) -> Image.Image:
    width, height = sprite.size
    holo = (0, 0)
    texture_details = (0, 0, width, height)
    image_details = (width, height)
    holo_alpha = 0.3

    holo_overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    holo_pixels = holo_overlay.load()

    for x in range(width):
        for y in range(height):
            texture_coords = (x / width, y / height)
            uv_x = (
                texture_coords[0] * image_details[0]
                - texture_details[0] * texture_details[2]
            ) / texture_details[2]
            uv_y = (
                texture_coords[1] * image_details[1]
                - texture_details[1] * texture_details[3]
            ) / texture_details[3]
            uv = (uv_x, uv_y)

            r, g, b, a = sprite.getpixel((x, y))
            if a == 0:
                continue

            hsl = colorsys.rgb_to_hls(0.5 * 0, 0.5 * 0, 0.5 * 1)
            # r_norm, g_norm, b_norm = r / 255.0, g / 255.0, b / 255.0
            # hsl = colorsys.rgb_to_hls(
            #     0.5 * r_norm + 0.5 * 0, 0.5 * g_norm + 0.5 * 0, 0.5 * b_norm + 0.5 * 1
            # )

            t = 0
            floored_uv_x = math.floor(uv_x * texture_details[2]) / texture_details[2]
            floored_uv_y = math.floor(uv_y * texture_details[3]) / texture_details[3]
            floored_uv = (floored_uv_x, floored_uv_y)
            uv_scaled_centered_x = (floored_uv[0] - 0.5) * 250.0
            uv_scaled_centered_y = (floored_uv[1] - 0.5) * 250.0
            uv_scaled_centered = (uv_scaled_centered_x, uv_scaled_centered_y)

            field_part1_x = uv_scaled_centered[0] + 50.0 * math.sin(-t / 143.6340)
            field_part1_y = uv_scaled_centered[1] + 50.0 * math.cos(-t / 99.4324)
            field_part1 = (field_part1_x, field_part1_y)
            field_part2_x = uv_scaled_centered[0] + 50.0 * math.cos(t / 53.1532)
            field_part2_y = uv_scaled_centered[1] + 50.0 * math.cos(t / 61.4532)
            field_part2 = (field_part2_x, field_part2_y)
            field_part3_x = uv_scaled_centered[0] + 50.0 * math.sin(-t / 87.53218)
            field_part3_y = uv_scaled_centered[1] + 50.0 * math.sin(-t / 49.0000)
            field_part3 = (field_part3_x, field_part3_y)

            field = (
                1.0
                + (
                    math.cos(
                        math.sqrt(field_part1[0] ** 2 + field_part1[1] ** 2) / 19.483
                    )
                    + math.sin(
                        math.sqrt(field_part2[0] ** 2 + field_part2[1] ** 2) / 33.155
                    )
                    * math.cos(field_part2[1] / 15.73)
                    + math.cos(
                        math.sqrt(field_part3[0] ** 2 + field_part3[1] ** 2) / 27.193
                    )
                    * math.sin(field_part3[0] / 21.92)
                )
            ) / 2.0

            res = 0.5 + 0.5 * math.cos(holo[0] * 2.612 + (field - 0.5) * 3.14)

            gridsize = 0.79
            fac = 0.5 * max(
                0.0,
                7.0 * abs(math.cos(uv_x * gridsize * 20.0)) - 6.0,
                max(
                    0.0,
                    7.0 * math.cos(uv_y * gridsize * 45.0 + uv_x * gridsize * 20.0)
                    - 6.0,
                ),
                max(
                    0.0,
                    7.0 * math.cos(uv_y * gridsize * 45.0 - uv_x * gridsize * 20.0)
                    - 6.0,
                ),
            )

            h = hsl[0] + res + fac
            l = hsl[1] * 1.3
            s = hsl[2] * 0.6 + 0.4

            modified_r, modified_g, modified_b = colorsys.hls_to_rgb(h, l, s)

            holo_pixels[x, y] = (
                int(max(0, min(1, modified_r * 0.9)) * 255),
                int(max(0, min(1, modified_g * 0.8)) * 255),
                int(max(0, min(1, modified_b * 1.2)) * 255),
                int(max(0, min(1, holo_alpha)) * 255),
            )

    return Image.alpha_composite(sprite, holo_overlay)


def _apply_polychrome(sprite: Image.Image) -> Image.Image:
    width, height = sprite.size
    polychrome_val = (0, 0)  # Static polychrome values (tilt0)
    texture_details = (0, 0, width, height)
    image_details = (width, height)

    polychrome_overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    overlay_pixels = polychrome_overlay.load()
    base_pixels = sprite.load()

    for x in range(width):
        for y in range(height):
            r, g, b, a = base_pixels[x, y]
            if a == 0:
                continue
            tex_r, tex_g, tex_b = r / 255.0, g / 255.0, b / 255.0

            brightness = 0.299 * tex_r + 0.587 * tex_g + 0.114 * tex_b

            low = min(tex_r, tex_g, tex_b)
            high = max(tex_r, tex_g, tex_b)
            delta = high - low

            saturation_fac = 1.0 - max(0.0, 0.05 * (1.1 - delta))
            saturated_r, saturated_g, saturated_b = (
                tex_r * saturation_fac,
                tex_g * saturation_fac,
                tex_b,
            )

            hsl = colorsys.rgb_to_hls(saturated_r, saturated_g, saturated_b)

            texture_coords = (x / width, y / height)
            uv_x = (
                texture_coords[0] * image_details[0]
                - texture_details[0] * texture_details[2]
            ) / texture_details[2]
            uv_y = (
                texture_coords[1] * image_details[1]
                - texture_details[1] * texture_details[3]
            ) / texture_details[3]
            uv = (uv_x, uv_y)

            floored_uv_x = math.floor(uv_x * texture_details[2]) / texture_details[2]
            floored_uv_y = math.floor(uv_y * texture_details[3]) / texture_details[3]
            floored_uv = (floored_uv_x, floored_uv_y)
            uv_scaled_centered_x = (floored_uv[0] - 0.5) * 50.0
            uv_scaled_centered_y = (floored_uv[1] - 0.5) * 50.0
            uv_scaled_centered = (uv_scaled_centered_x, uv_scaled_centered_y)

            field_part1_x = uv_scaled_centered[0] + 50.0 * math.sin(0)
            field_part1_y = uv_scaled_centered[1] + 50.0 * math.cos(0)
            field_part1 = (field_part1_x, field_part1_y)
            field_part2_x = uv_scaled_centered[0] + 50.0 * math.cos(0)
            field_part2_y = uv_scaled_centered[1] + 50.0 * math.cos(0)
            field_part2 = (field_part2_x, field_part2_y)
            field_part3_x = uv_scaled_centered[0] + 50.0 * math.sin(0)
            field_part3_y = uv_scaled_centered[1] + 50.0 * math.sin(0)
            field_part3 = (field_part3_x, field_part3_y)

            field = (
                1.0
                + (
                    math.cos(
                        math.sqrt(field_part1[0] ** 2 + field_part1[1] ** 2) / 19.483
                    )
                    + math.sin(
                        math.sqrt(field_part2[0] ** 2 + field_part2[1] ** 2) / 33.155
                    )
                    * math.cos(field_part2[1] / 15.73)
                    + math.cos(
                        math.sqrt(field_part3[0] ** 2 + field_part3[1] ** 2) / 27.193
                    )
                    * math.sin(field_part3[0] / 21.92)
                )
            ) / 2.0

            res = 0.5 + 0.5 * math.cos(polychrome_val[0] * 2.612 + (field - 0.5) * 3.14)

            h = hsl[0] + res + polychrome_val[1] * 0.04
            l = min(0.6, hsl[1] + 0.5)
            s = hsl[2] + 0.5

            modified_r, modified_g, modified_b = colorsys.hls_to_rgb(h, l, s)

            effect_intensity = 0.1 if brightness > 0.9 else 0.5
            # effect_intensity = 0.8
            overlay_r = modified_r
            overlay_g = modified_g
            overlay_b = modified_b
            overlay_alpha = effect_intensity

            overlay_pixels[x, y] = (
                int(max(0, min(1, overlay_r)) * 255),
                int(max(0, min(1, overlay_g)) * 255),
                int(max(0, min(1, overlay_b)) * 255),
                int(overlay_alpha * 255),
            )

    return Image.alpha_composite(sprite, polychrome_overlay)


def _apply_negative(sprite: Image.Image) -> Image.Image:
    width, height = sprite.size
    new_sprite = Image.new("RGBA", (width, height))

    for x in range(width):
        for y in range(height):
            r, g, b, a = sprite.getpixel((x, y))

            # if a <= 0:
            #     new_sprite.putpixel((x, y), (0, 0, 0, 0))
            #     continue

            r_norm, g_norm, b_norm = r / 255.0, g / 255.0, b / 255.0

            h, l, s = colorsys.rgb_to_hls(r_norm, g_norm, b_norm)

            l = 1.0 - l
            h = -h + 0.2
            # h %= 1.0

            r_new_norm, g_new_norm, b_new_norm = colorsys.hls_to_rgb(h, l, s)

            constant_r = 79 / 255.0
            constant_g = 99 / 255.0
            constant_b = 103 / 255.0

            r_new_norm += 0.8 * constant_r
            g_new_norm += 0.8 * constant_g
            b_new_norm += 0.8 * constant_b

            r_new = int(r_new_norm * 255)
            g_new = int(g_new_norm * 255)
            b_new = int(b_new_norm * 255)

            new_sprite.putpixel((x, y), (r_new, g_new, b_new, a))

    return new_sprite


def _get_hologram_sprite(face_sprite):
    def create_hologram_effect(image):
        # Convert to RGBA if not already
        image = image.convert("RGBA")

        # Create glow effect
        glow = image.filter(ImageFilter.GaussianBlur(10))
        glow_data = np.array(glow)

        # Create base cyan tint
        cyan_overlay = Image.new("RGBA", image.size, (0, 255, 255, 0))

        # Create the final composition
        result = Image.new("RGBA", image.size, (0, 0, 0, 0))

        # Get image data as numpy arrays
        img_data = np.array(image)
        cyan_data = np.array(cyan_overlay)

        # Create the hologram effect
        for y in range(image.height):
            for x in range(image.width):
                alpha = img_data[y, x, 3]
                if alpha > 250:  # If pixel is fully opaque (card background)
                    result.putpixel((x, y), (0, 0, 0, 0))
                elif alpha < 1:  # If pixel is fully transparent
                    # Add cyan glow
                    glow_alpha = int(glow_data[y, x, 3] * 0.4)  # Reduce glow intensity
                    result.putpixel((x, y), (0, 255, 255, glow_alpha))
                else:
                    # Semi-transparent pixels (card details)
                    # Add slight cyan tint to existing colors
                    r, g, b = img_data[y, x, 0:3]
                    new_color = (
                        int(r * 0.8),  # Reduce red
                        int(g * 1.1),  # Boost green slightly
                        int(b * 1.1),  # Boost blue slightly
                        alpha,
                    )
                    result.putpixel((x, y), new_color)

        # Add final glow
        glow_layer = result.filter(ImageFilter.GaussianBlur(10))
        glow_layer.putalpha(ImageEnhance.Brightness(glow_layer.split()[3]).enhance(0.3))

        return Image.alpha_composite(result, glow_layer)

    # Boost brightness of face
    hologram_sprite = create_hologram_effect(face_sprite)
    hologram_sprite = ImageEnhance.Brightness(hologram_sprite).enhance(1.1)

    # Create new transparent image for composition
    result = Image.new("RGBA", hologram_sprite.size, (0, 0, 0, 0))
    result = Image.alpha_composite(result, hologram_sprite)

    return result


def get_sprite(
    item: BaseJoker | Consumable | Card | Voucher | Stake | Tag | Blind | Deck | Pack,
    card_back: Deck = Deck.RED,
    as_image: bool = True,
) -> bytes:
    match item:
        case BaseJoker():
            match item:
                case HalfJoker():
                    WIDTH, HEIGHT = DEFAULT_CARD_WIDTH, int(DEFAULT_CARD_HEIGHT // 1.7)
                case SquareJoker():
                    WIDTH, HEIGHT = DEFAULT_CARD_WIDTH, DEFAULT_CARD_WIDTH
                case Photograph():
                    WIDTH, HEIGHT = DEFAULT_CARD_WIDTH, int(DEFAULT_CARD_HEIGHT // 1.2)
                case _:
                    WIDTH, HEIGHT = DEFAULT_CARD_WIDTH, DEFAULT_CARD_HEIGHT

            if item.is_flipped:
                if isinstance(item, WeeJoker):
                    WIDTH, HEIGHT = int(WIDTH * 0.7), int(HEIGHT * 0.7)
                sprite = get_sprite(card_back)
                sprite = sprite.resize((WIDTH, HEIGHT))
            else:
                with open("resources/textures/Jokers.txt") as file:
                    joker_sheet = Image.open(io.BytesIO(base64.b64decode(file.read())))
                with open("resources/textures/stickers.txt") as file:
                    stickers_sheet = Image.open(
                        io.BytesIO(base64.b64decode(file.read()))
                    )

                i, j = JOKER_COORDINATES.get(type(item), [0, 0])
                x1, y1 = DEFAULT_CARD_WIDTH * j, DEFAULT_CARD_HEIGHT * i
                x2, y2 = x1 + WIDTH, y1 + HEIGHT
                sprite = joker_sheet.crop((x1, y1, x2, y2))

                sprite = _apply_edition(sprite, item.edition)

                match item:
                    case WeeJoker():
                        WIDTH, HEIGHT = int(WIDTH * 0.7), int(HEIGHT * 0.7)
                        sprite = sprite.resize((WIDTH, HEIGHT))
                    case Canio() | Triboulet() | Yorick() | Chicot() | Perkeo():
                        i, j = i + 1, j
                        x1, y1 = DEFAULT_CARD_WIDTH * j, DEFAULT_CARD_HEIGHT * i
                        x2, y2 = x1 + WIDTH, y1 + HEIGHT
                        face_sprite = joker_sheet.crop((x1, y1, x2, y2))
                        face_shadow_sprite = Image.new(
                            "RGBA", face_sprite.size, (0, 0, 0, 0)
                        )
                        face_shadow_sprite.paste((0, 0, 0, 70), (0, 5), face_sprite)
                        sprite = Image.alpha_composite(sprite, face_shadow_sprite)
                        sprite = Image.alpha_composite(sprite, face_sprite)
                    case Hologram():
                        i, j = 9, 2
                        x1, y1 = DEFAULT_CARD_WIDTH * j, DEFAULT_CARD_HEIGHT * i
                        x2, y2 = x1 + WIDTH, y1 + HEIGHT
                        face_sprite = joker_sheet.crop((x1, y1, x2, y2))
                        hologram_sprite = _get_hologram_sprite(face_sprite)
                        sprite = Image.alpha_composite(sprite, hologram_sprite)

                if item.is_eternal:
                    i, j = 0, 0
                    x1, y1 = DEFAULT_CARD_WIDTH * j, DEFAULT_CARD_HEIGHT * i
                    x2, y2 = x1 + WIDTH, y1 + HEIGHT
                    eternal_sprite = stickers_sheet.crop((x1, y1, x2, y2))
                    sprite = Image.alpha_composite(sprite, eternal_sprite)
                elif item.is_perishable:
                    i, j = 2, 0
                    x1, y1 = DEFAULT_CARD_WIDTH * j, DEFAULT_CARD_HEIGHT * i
                    x2, y2 = x1 + WIDTH, y1 + HEIGHT
                    perishable_sprite = stickers_sheet.crop((x1, y1, x2, y2))
                    sprite = Image.alpha_composite(sprite, perishable_sprite)
                if item.is_rental:
                    i, j = 2, 1
                    x1, y1 = DEFAULT_CARD_WIDTH * j, DEFAULT_CARD_HEIGHT * i
                    x2, y2 = x1 + WIDTH, y1 + HEIGHT
                    rental_sprite = stickers_sheet.crop((x1, y1, x2, y2))
                    sprite = Image.alpha_composite(sprite, rental_sprite)

                if item.is_debuffed:
                    sprite = _apply_debuff(sprite)
        case Consumable():
            with open("resources/textures/Tarots.txt") as file:
                consumable_sheet = Image.open(io.BytesIO(base64.b64decode(file.read())))

            i, j = CONSUMABLE_COORDINATES[item.card]
            x1, y1 = DEFAULT_CARD_WIDTH * j, DEFAULT_CARD_HEIGHT * i
            x2, y2 = x1 + DEFAULT_CARD_WIDTH, y1 + DEFAULT_CARD_HEIGHT
            sprite = consumable_sheet.crop((x1, y1, x2, y2))

            sprite = _apply_edition(
                sprite, Edition.NEGATIVE if item.is_negative else Edition.BASE
            )

            if item.card is Spectral.THE_SOUL:
                with open("resources/textures/Enhancers.txt") as file:
                    enhancers_sheet = Image.open(
                        io.BytesIO(base64.b64decode(file.read()))
                    )
                i, j = 1, 0
                x1, y1 = DEFAULT_CARD_WIDTH * j, DEFAULT_CARD_HEIGHT * i
                x2, y2 = x1 + DEFAULT_CARD_WIDTH, y1 + DEFAULT_CARD_HEIGHT
                soul_sprite = enhancers_sheet.crop((x1, y1, x2, y2))
                soul_shadow_sprite = Image.new("RGBA", soul_sprite.size, (0, 0, 0, 0))
                soul_shadow_sprite.paste((0, 0, 0, 70), (0, 5), soul_sprite)
                sprite = Image.alpha_composite(sprite, soul_shadow_sprite)
                sprite = Image.alpha_composite(sprite, soul_sprite)
        case Card():
            if item.is_face_down:
                sprite = get_sprite(card_back)
            else:
                with open("resources/textures/8BitDeck.txt") as file:
                    deck_sheet = Image.open(io.BytesIO(base64.b64decode(file.read())))
                with open("resources/textures/Enhancers.txt") as file:
                    enhancers_sheet = Image.open(
                        io.BytesIO(base64.b64decode(file.read()))
                    )

                i, j = ENHANCER_COORDINATES.get(item.enhancement, (0, 1))
                x1, y1 = DEFAULT_CARD_WIDTH * j, DEFAULT_CARD_HEIGHT * i
                x2, y2 = x1 + DEFAULT_CARD_WIDTH, y1 + DEFAULT_CARD_HEIGHT
                back_sprite = enhancers_sheet.crop((x1, y1, x2, y2))

                if not item.is_stone_card:
                    i, j = SUIT_ROWS[item.suit], RANK_COLUMNS[item.rank]
                    x1, y1 = DEFAULT_CARD_WIDTH * j, DEFAULT_CARD_HEIGHT * i
                    x2, y2 = x1 + DEFAULT_CARD_WIDTH, y1 + DEFAULT_CARD_HEIGHT
                    card_sprite = deck_sheet.crop((x1, y1, x2, y2))
                    sprite = Image.alpha_composite(back_sprite, card_sprite)
                else:
                    sprite = back_sprite

                sprite = _apply_edition(sprite, item.edition)

                if item.seal is not None:
                    i, j = ENHANCER_COORDINATES[item.seal]
                    x1, y1 = DEFAULT_CARD_WIDTH * j, DEFAULT_CARD_HEIGHT * i
                    x2, y2 = x1 + DEFAULT_CARD_WIDTH, y1 + DEFAULT_CARD_HEIGHT
                    seal_sprite = enhancers_sheet.crop((x1, y1, x2, y2))
                    sprite = Image.alpha_composite(sprite, seal_sprite)

                if item.is_debuffed:
                    sprite = _apply_debuff(sprite)
        case Voucher():
            with open("resources/textures/Vouchers.txt") as file:
                voucher_sheet = Image.open(io.BytesIO(base64.b64decode(file.read())))

            i, j = VOUCHER_COORDINATES[item]
            x1, y1 = DEFAULT_CARD_WIDTH * j, DEFAULT_CARD_HEIGHT * i
            x2, y2 = x1 + DEFAULT_CARD_WIDTH, y1 + DEFAULT_CARD_HEIGHT
            sprite = voucher_sheet.crop((x1, y1, x2, y2))
        case Stake():
            with open("resources/textures/chips.txt") as file:
                chips_sheet = Image.open(io.BytesIO(base64.b64decode(file.read())))

            i, j = CHIPS_COORDINATES[item]
            x1, y1 = DEFAULT_CHIP_WIDTH * j, DEFAULT_CHIP_HEIGHT * i
            x2, y2 = x1 + DEFAULT_CHIP_WIDTH, y1 + DEFAULT_CHIP_HEIGHT
            sprite = chips_sheet.crop((x1, y1, x2, y2))
        case Tag():
            with open("resources/textures/tags.txt") as file:
                tags_sheet = Image.open(io.BytesIO(base64.b64decode(file.read())))

            i, j = TAG_COORDINATES[item]
            x1, y1 = DEFAULT_TAG_WIDTH * j, DEFAULT_TAG_HEIGHT * i
            x2, y2 = x1 + DEFAULT_TAG_WIDTH, y1 + DEFAULT_TAG_HEIGHT
            sprite = tags_sheet.crop((x1, y1, x2, y2))
        case Blind():
            with open("resources/textures/BlindChips.txt") as file:
                blind_chips_sheet = Image.open(
                    io.BytesIO(base64.b64decode(file.read()))
                )

            i, j = BLIND_ROWS[item], 0
            x1, y1 = DEFAULT_BLIND_WIDTH * j, DEFAULT_BLIND_HEIGHT * i
            x2, y2 = x1 + DEFAULT_BLIND_WIDTH, y1 + DEFAULT_BLIND_HEIGHT
            sprite = blind_chips_sheet.crop((x1, y1, x2, y2))
        case Deck():
            with open("resources/textures/Enhancers.txt") as file:
                enhancers_sheet = Image.open(io.BytesIO(base64.b64decode(file.read())))

            i, j = ENHANCER_COORDINATES[item]
            x1, y1 = DEFAULT_CARD_WIDTH * j, DEFAULT_CARD_HEIGHT * i
            x2, y2 = x1 + DEFAULT_CARD_WIDTH, y1 + DEFAULT_CARD_HEIGHT
            sprite = enhancers_sheet.crop((x1, y1, x2, y2))
        case Pack():
            with open("resources/textures/boosters.txt") as file:
                pack_sheet = Image.open(io.BytesIO(base64.b64decode(file.read())))

            # i, j = r.choice(PACK_COORDINATES[item])
            i, j = PACK_COORDINATES[item][0]
            x1, y1 = DEFAULT_CARD_WIDTH * j, DEFAULT_CARD_HEIGHT * i
            x2, y2 = x1 + DEFAULT_CARD_WIDTH, y1 + DEFAULT_CARD_HEIGHT
            sprite = pack_sheet.crop((x1, y1, x2, y2))

    if as_image:
        return sprite
    with io.BytesIO() as buffer:
        sprite.save(buffer, "png")
        return buffer.getvalue()
