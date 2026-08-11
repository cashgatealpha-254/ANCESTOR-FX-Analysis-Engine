from environment.deep_context_store import DeepContextStore
from environment.fast_forward_engine import FastForwardEngine
from environment.context_comparator import ContextComparator
from environment.context_adapter import ContextAdapter


class ContextOrchestrator:

    def __init__(self):

        self.store = DeepContextStore()

        self.fast_forward = FastForwardEngine()

        self.comparator = ContextComparator()

        self.adapter = ContextAdapter()

    # ==================================================
    # BUILD CURRENT CONTEXT
    # ==================================================

    def build_context(
        self,
        symbol,
        horizon,
        deep_context=None
    ):

        # ==============================================
        # LOAD STORED DEEP CONTEXT
        # ==============================================

        stored_context = self.store.load(
            symbol,
            horizon
        )

        # Use explicitly supplied deep context
        # when available; otherwise use stored context.
        if deep_context is None:

            deep_context = stored_context

        # ==============================================
        # FAST-FORWARD ANALYSIS
        # ==============================================

        recent_context = self.fast_forward.analyze(
            symbol,
            horizon
        )

        # ==============================================
        # PREPARE COMPARISON
        # ==============================================

        previous_context = None
        current_context = None

        if isinstance(
            stored_context,
            dict
        ):

            previous_context = (
                stored_context.get(
                    "context",
                    {}
                )
            )

        if isinstance(
            deep_context,
            dict
        ):

            current_context = (
                deep_context.get(
                    "context",
                    deep_context
                )
            )

        # ==============================================
        # COMPARE
        # ==============================================

        changes = self.comparator.compare(
            previous_context,
            current_context
        )

        # ==============================================
        # ADAPT
        # ==============================================

        return self.adapter.build(
            deep_context=current_context,
            recent_context=recent_context,
            changes=changes
        )