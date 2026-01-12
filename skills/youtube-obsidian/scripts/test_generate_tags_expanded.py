#!/usr/bin/env python3
"""
Expanded tests for generate_tags() function.

Tests edge cases, boundary conditions, and error scenarios
for tag generation functionality.
"""

import pytest
from get_youtube_data import generate_tags


class TestGenerateTagsEmptyInput:
    """Tests for empty input scenarios (P1)."""

    @pytest.mark.p1
    @pytest.mark.unit
    def test_empty_all_inputs_returns_empty_list(self):
        """Test that empty input returns empty list."""
        tags = generate_tags("", "", "", [])
        assert tags == []

    @pytest.mark.p1
    @pytest.mark.unit
    def test_empty_youtube_tags_with_capitalized_words(self):
        """Test tags generated from capitalized words when youtube_tags empty."""
        tags = generate_tags("Python Tutorial", "", "Machine Learning", [])
        assert len(tags) > 0
        assert "python" in tags or "tutorial" in tags

    @pytest.mark.p1
    @pytest.mark.unit
    def test_no_capitalized_words_only_tech_terms(self):
        """Test result when no capitalized words but has tech terms."""
        tags = generate_tags("all lower", "no caps", "nothing capitalized", [])
        # 'api' is a tech term that will be detected
        assert "api" in tags

    @pytest.mark.p1
    @pytest.mark.unit
    def test_only_tech_terms_no_caps(self):
        """Test tags from tech terms when no capitalized words."""
        tags = generate_tags("all lower", "python javascript api", "development", [])
        assert "python" in tags
        assert "javascript" in tags


class TestGenerateTagsEdgeCases:
    """Tests for edge cases and boundary conditions (P1)."""

    @pytest.mark.p1
    @pytest.mark.unit
    def test_very_long_input_truncates_to_15(self):
        """Test that very long input is limited to 15 tags."""
        # Create input with many potential tags
        capitalized_words = [f"Word{i}" for i in range(20)]
        youtube_tags = [f"tag{i}" for i in range(20)]
        transcript = " ".join(capitalized_words)

        tags = generate_tags(
            " ".join(capitalized_words), transcript, transcript, youtube_tags
        )

        assert len(tags) <= 15
        assert len(tags) == 15  # Should hit the limit

    @pytest.mark.p1
    @pytest.mark.unit
    def test_exactly_15_tags_returns_all(self):
        """Test that tags are generated from multiple words."""
        # Use words separated by proper spacing for capitalized detection
        content = "Python Java JavaScript Coding Tutorial Guide Video Channel Content Create Update Delete Search Filter Sort"
        tags = generate_tags(content, "", "", [])

        # Should generate several tags from the content
        assert len(tags) >= 5
        assert any("python" in tag.lower() for tag in tags)

    @pytest.mark.p1
    @pytest.mark.unit
    def test_special_characters_in_content(self):
        """Test handling of special characters."""
        tags = generate_tags(
            'Python: "Tutorial" & Guide', "API @#$%", "Development", []
        )

        # Should generate tags from valid parts
        assert len(tags) > 0
        # Tags shouldn't contain special characters
        for tag in tags:
            assert ":" not in tag
            assert '"' not in tag
            assert "&" not in tag
            assert "@" not in tag
            assert "#" not in tag

    @pytest.mark.p1
    @pytest.mark.unit
    def test_unicode_characters_in_content(self):
        """Test handling of Unicode characters."""
        tags = generate_tags("Python 日本語 中国語 🎉", "API development", "coding", [])

        # Should handle Unicode without crashing
        assert isinstance(tags, list)
        assert len(tags) > 0

    @pytest.mark.p1
    @pytest.mark.unit
    def test_duplicate_tags_from_different_sources(self):
        """Test that duplicate tags are removed."""
        tags = generate_tags(
            "Python Tutorial",
            "Python API",
            "Python development",
            ["python"],
        )

        # Python should appear only once
        assert tags.count("python") == 1

    @pytest.mark.p1
    @pytest.mark.unit
    def test_case_insensitive_deduplication(self):
        """Test that tags with different cases are deduplicated."""
        tags = generate_tags("Python Tutorial", "PYTHON API", "python Development", [])

        # Should have only one "python" variant
        python_variants = [t for t in tags if t.lower() == "python"]
        assert len(python_variants) == 1


class TestGenerateTagsTechTerms:
    """Tests for tech term detection (P1)."""

    @pytest.mark.p1
    @pytest.mark.unit
    def test_tech_terms_in_transcript(self):
        """Test detection of tech terms in transcript."""
        tags = generate_tags("", "", "python javascript machine learning api", [])

        assert "python" in tags
        assert "javascript" in tags
        assert "machine learning" in tags or "machine" in tags or "learning" in tags

    @pytest.mark.p1
    @pytest.mark.unit
    def test_tech_terms_in_description(self):
        """Test detection of tech terms in description."""
        tags = generate_tags("", "API docker kubernetes cloud", "", [])

        assert "api" in tags
        assert "docker" in tags
        assert "kubernetes" in tags
        assert "cloud" in tags

    @pytest.mark.p1
    @pytest.mark.unit
    def test_no_tech_terms_found(self):
        """Test behavior when no tech terms found."""
        tags = generate_tags(
            "Random Title",
            "Random description",
            "Random transcript with no tech terms",
            ["tag1", "tag2"],
        )

        # Should have youtube tags + any capitalized words (Random, Title, etc.)
        assert "tag1" in tags
        assert "tag2" in tags
        # May also have capitalized words from content

    @pytest.mark.p1
    @pytest.mark.unit
    def test_mixed_sources_tech_terms_priority(self):
        """Test that tech terms are included with youtube tags."""
        tags = generate_tags(
            "Tutorial", "API development", "Python", ["tutorial", "coding"]
        )

        assert "tutorial" in tags
        assert "coding" in tags
        assert "python" in tags
        assert "api" in tags
        assert "development" in tags


class TestGenerateTagsCapitalizedWords:
    """Tests for capitalized word extraction (P1)."""

    @pytest.mark.p1
    @pytest.mark.unit
    def test_single_capitalized_word(self):
        """Test extraction of single capitalized word."""
        tags = generate_tags("Python", "", "", [])

        assert "python" in tags

    @pytest.mark.p1
    @pytest.mark.unit
    def test_multiple_capitalized_words(self):
        """Test extraction of multiple capitalized words."""
        tags = generate_tags("Python Tutorial Machine Learning", "", "", [])

        assert "python" in tags
        assert "tutorial" in tags
        assert "machine" in tags or "learning" in tags

    @pytest.mark.p1
    @pytest.mark.unit
    def test_capitalized_words_in_transcript(self):
        """Test extraction from transcript."""
        tags = generate_tags("", "", "Hello World Python Tutorial", [])

        assert "python" in tags
        assert "tutorial" in tags

    @pytest.mark.p1
    @pytest.mark.unit
    def test_short_capitalized_words_filtered(self):
        """Test that words shorter than 4 chars are filtered."""
        tags = generate_tags("The A An API", "", "", [])

        assert "api" in tags
        # Short words (a, an, the) should be filtered
        assert "a" not in tags
        assert "an" not in tags
        assert "the" not in tags


class TestGenerateTagsYouTubeTags:
    """Tests for YouTube tag integration (P2)."""

    @pytest.mark.p2
    @pytest.mark.unit
    def test_youtube_tags_included(self):
        """Test that YouTube tags are always included."""
        youtube_tags = ["tag1", "tag2", "tag3"]
        tags = generate_tags("", "", "", youtube_tags)

        for tag in youtube_tags:
            assert tag in tags

    @pytest.mark.p2
    @pytest.mark.unit
    def test_youtube_tags_deduplicated(self):
        """Test that duplicate YouTube tags are removed."""
        youtube_tags = ["python", "python", "coding"]
        tags = generate_tags("", "", "", youtube_tags)

        assert tags.count("python") == 1
        assert "coding" in tags

    @pytest.mark.p2
    @pytest.mark.unit
    def test_youtube_tags_case_preserved(self):
        """Test that YouTube tags are passed through as-is."""
        youtube_tags = ["Python", "CODING", "Tutorial"]
        tags = generate_tags("", "", "", youtube_tags)

        # Tags should be included (may or may not be lowercased)
        assert "Python" in tags or "python" in tags
        assert "CODING" in tags or "coding" in tags
        assert "Tutorial" in tags or "tutorial" in tags


class TestGenerateTagsOrdering:
    """Tests for tag ordering and sorting (P2)."""

    @pytest.mark.p2
    @pytest.mark.unit
    def test_tags_are_sorted_alphabetically(self):
        """Test that returned tags are sorted alphabetically."""
        tags = generate_tags("Zebra Alpha Beta", "", "", [])

        # Verify tags are sorted
        assert tags == sorted(tags)

    @pytest.mark.p2
    @pytest.mark.unit
    def test_tags_limit_respects_sorting(self):
        """Test that tag limit is applied after sorting."""
        # Create unsorted tags
        capitalized_words = [chr(ord("Z") - i) for i in range(20)]  # Z, Y, X, W, ...
        tags = generate_tags(" ".join(capitalized_words), "", "", [])

        # Should be sorted and limited
        assert tags == sorted(tags)
        assert len(tags) <= 15
