from usembridge.policy import Action, choose_action


def test_policy_bins():
    assert choose_action(0.1) is Action.VERIFY
    assert choose_action(0.4) is Action.COMPARE_REPAIR
    assert choose_action(0.7) is Action.CLARIFY
    assert choose_action(0.9) is Action.ABSTAIN


def test_critical_unresolved_never_verifies():
    assert choose_action(0.1, unresolved_critical=True) is Action.CLARIFY
