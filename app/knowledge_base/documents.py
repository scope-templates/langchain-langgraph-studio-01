"""The library's knowledge base content.

In production these are authored in the handbook CMS and synced here on deploy.
For now they live in-process so the service has no external dependency.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List


@dataclass(frozen=True)
class Document:
    doc_id: str
    title: str
    url: str
    tags: List[str] = field(default_factory=list)
    body: str = ""


RAW_DOCUMENTS: List[Document] = [
    Document(
        doc_id="handbook-membership",
        title="Membership and borrowing basics",
        url="/handbook/membership",
        tags=["membership", "borrowing", "policy"],
        body=(
            "Membership at the Thimbleby Community Tool Library is open to any "
            "resident aged eighteen or older with proof of a local address. "
            "An annual membership costs twelve dollars and covers one household. "
            "Members may borrow up to three tools at a time. Power tools count "
            "as two items against this limit. The standard loan period is seven "
            "days. You can renew a loan once for another seven days if nobody "
            "has placed a hold on the tool. Loans that run past their due date "
            "accrue a late fee of fifty cents per tool per day, capped at the "
            "replacement value of the tool."
        ),
    ),
    Document(
        doc_id="care-drills",
        title="Caring for cordless drills",
        url="/guides/cordless-drills",
        tags=["tool-care", "power-tools", "drills", "batteries"],
        body=(
            "Cordless drills are our most borrowed power tool, so please return "
            "them clean and charged. Store the battery at roughly half charge if "
            "you keep the drill overnight; a fully drained lithium battery can "
            "be hard to revive. Never force a stuck bit. If the chuck will not "
            "loosen, bring the drill to the front desk rather than using pliers. "
            "Wipe grit off the vents before returning. Report any smell of hot "
            "plastic immediately; we will retire the tool for inspection. "
            "Spare batteries and chargers live in the cage behind the counter "
            "and are lent only with the matching drill."
        ),
    ),
    Document(
        doc_id="care-ladders",
        title="Ladder safety and returns",
        url="/guides/ladders",
        tags=["tool-care", "ladders", "safety"],
        body=(
            "Before climbing, open the ladder fully and lock both spreader "
            "braces. Set it on firm, level ground and keep three points of "
            "contact at all times. Do not stand on the top two rungs of a step "
            "ladder. We do not lend ladders taller than eight feet to members "
            "without a completed safety orientation. Fiberglass ladders are "
            "required for any work near electrical lines. On return, inspect the "
            "feet for cracks and flag any bent rungs so staff can tag the ladder "
            "out of service."
        ),
    ),
    Document(
        doc_id="care-canning",
        title="Canning kit cleaning and food safety",
        url="/guides/canning-kits",
        tags=["tool-care", "canning", "kitchen", "food-safety"],
        body=(
            "Our canning kits include a water-bath pot, a jar rack, a funnel, a "
            "bubble remover and a magnetic lid lifter. Pressure canner gauges "
            "must be tested each season; a kit with an untested gauge is marked "
            "with a yellow tag and lent for water-bath use only. Wash every "
            "piece in hot soapy water before returning. Do not return a kit with "
            "food residue or the deposit is withheld. Replace any cracked jars "
            "from your own supply. We do not lend used lids; bring new flats for "
            "each batch to ensure a safe seal."
        ),
    ),
    Document(
        doc_id="care-sewing",
        title="Sewing machine setup and threading",
        url="/guides/sewing-machines",
        tags=["tool-care", "sewing", "textiles"],
        body=(
            "Each sewing machine goes out with its foot pedal, power cord, a "
            "general purpose foot and three bobbins. Thread the upper path with "
            "the presser foot raised so the tension discs stay open. Wind "
            "bobbins evenly and insert them so the thread feeds counterclockwise. "
            "If stitches skip, change the needle before adjusting tension; a "
            "dull or bent needle is the usual culprit. Return the machine with "
            "the needle removed and the bed cover closed. Replace used needles "
            "from the desk at no charge."
        ),
    ),
    Document(
        doc_id="policy-holds",
        title="Holds, waitlists and no-shows",
        url="/handbook/holds",
        tags=["policy", "holds", "borrowing"],
        body=(
            "When a tool is out, you may place a hold and we will text you when "
            "it returns. A held tool is kept at the desk for two days before it "
            "moves to the next member in line. Three no-shows in a season pauses "
            "your hold privileges for thirty days. Seasonal tools such as snow "
            "shovels and hedge trimmers often have long waitlists; the catalog "
            "shows your position in line. You cannot hold a tool you already have "
            "on loan, and you cannot hold more than two tools at once."
        ),
    ),
    Document(
        doc_id="policy-damage",
        title="Damaged and lost tools",
        url="/handbook/damage",
        tags=["policy", "damage", "fees"],
        body=(
            "Normal wear is expected and never charged. If a tool is damaged "
            "beyond normal wear, we assess a repair fee based on parts and bench "
            "time, never exceeding replacement value. A lost tool is billed at "
            "its listed replacement value; if you later find and return it in "
            "working order within sixty days we refund the charge minus a small "
            "restocking fee. Tell us about damage at return instead of hiding "
            "it; honest reports keep fees low for everyone and help us keep the "
            "collection safe."
        ),
    ),
    Document(
        doc_id="hours-location",
        title="Hours, location and parking",
        url="/handbook/hours",
        tags=["hours", "location", "visiting"],
        body=(
            "We are at 14 Marrow Lane, in the rear unit behind the old creamery. "
            "We open Tuesday through Saturday from ten in the morning to six in "
            "the evening, and stay open until eight on Thursdays. We are closed "
            "Sunday and Monday and on public holidays. Free two-hour street "
            "parking is available on Marrow Lane; the lot across the street is "
            "permit only. Returns can be dropped in the covered bin to the left "
            "of the door when we are closed, except for power tools and canning "
            "kits, which must be handed to staff."
        ),
    ),
]
