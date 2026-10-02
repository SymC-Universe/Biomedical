from nsd_engine.v02_nb23_suite import build_member, suite_identity_summary


def test_frozen_suite_constructs_without_target_evaluation():
    s=suite_identity_summary()
    assert s["member_count"]==18
    assert s["scientific_adjudication"]=="NOT_PERFORMED_BY_GITHUB"
    for case_id in s["case_ids"]:
        m=build_member(case_id)
        assert m["case_id"]==case_id
        assert "kind" in m
