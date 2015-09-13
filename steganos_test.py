import steganos
import pytest

@pytest.mark.parametrize('length, expected', [
    (3, 'abc'),
    (5, 'abcab'),
    (2, 'ab')
])
def test_repeated_string(length, expected):
    assert expected == steganos.repeat('abc', length) 

@pytest.mark.parametrize('length, expected', [
    (3, ['a', 'b', 'c']),
    (5, ['a', 'b', 'c', 'a', 'b']),
    (2, ['a', 'b'])
])
def test_repeated_list(length, expected):
    assert expected == steganos.repeat(['a', 'b', 'c'], length) 

def test_get_all_branchpoints_finds_matching_quotes():
    # given
    text = '"Hello," he said.'

    # when 
    result = steganos.get_all_branchpoints(text)

    # then
    assert result == [[(0, 0, "'"), (7, 7, "'")]]

def test_filter_by_bits():
    # given
    bits = '101'
    xs = ['a', 'b', 'c']

    # when 
    result = steganos.filter_by_bits(xs, bits)

    # then
    assert result == ['a', 'c']

def test_make_change_for_single_change():
    # given 
    text = 'This is his dog.'
    changes = [(9, 10, 'er')]

    # when
    result = steganos.make_changes(text, changes)

    # then
    assert result == 'This is her dog.'

def test_make_changes_for_two_changes():
    # given
    text = 'This is his dog.'
    changes = [(9, 10, 'er'), (12, 14, 'cat')]

    # when
    result = steganos.make_changes(text, changes)

    # then
    assert result == 'This is her cat.'

def test_make_changes_when_change_is_different_length():
    # given
    text = 'This is just a sample string.'
    changes = [(22, 27, 'text'), (0, 3, 'It')]

    # when
    result = steganos.make_changes(text, changes)

    # then
    assert result == 'It is just a sample text.'

def test_execute_branchpoints_when_one_is_sandwiched():
    # given 
    text = '"How is she?" he asked.'
    branchpoints = [
        [(0, 0, "'"), (12, 12, "'")],
        [(8, 8, '')]
    ]

    # when 
    result = steganos.execute_branchpoints(branchpoints, text)

    # then
    assert result == "'How is he?' he asked."

def test_encode():
    # given
    text = '"How is she?" he asked.'
    bits = '1'

    # when
    result = steganos.encode(bits, text)

    # then
    assert result == "'How is she?' he asked."
