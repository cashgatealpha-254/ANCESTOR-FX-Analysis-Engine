from core.service_registry import ServiceRegistry

from brain.memory import MarketMemory
from brain.replay import ReplayEngine
from brain.patterns import PatternEngine
from brain.coach import CoachEngine
from brain.behavior import BehaviorEngine
from brain.dna import TraderDNA
from brain.evolution import StrategyEvolution
from brain.replay_studio import ReplayStudio
from brain.intelligence import IntelligenceCore


class Container:

    def __init__(self):

        self.registry = ServiceRegistry()

        self._register()

    def _register(self):

        self.registry.register(

            "memory",

            MarketMemory()

        )

        self.registry.register(

            "replay",

            ReplayEngine()

        )

        self.registry.register(

            "patterns",

            PatternEngine()

        )

        self.registry.register(

            "coach",

            CoachEngine()

        )

        self.registry.register(

            "behavior",

            BehaviorEngine()

        )

        self.registry.register(

            "dna",

            TraderDNA()

        )

        self.registry.register(

            "evolution",

            StrategyEvolution()

        )

        self.registry.register(

            "studio",

            ReplayStudio()

        )

        self.registry.register(

            "intelligence",

            IntelligenceCore()

        )

    def get(self, name):

        return self.registry.get(name)