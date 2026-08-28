from dobby.observability import configure_logging, get_logger


def test_info_level_filters_debug():
    configure_logging("INFO")
    logger = get_logger("test")

    assert logger.is_enabled_for(10) is False


def test_debug_level_allows_debug():
    configure_logging("DEBUG")
    logger = get_logger("test")

    assert logger.is_enabled_for(10) is True
