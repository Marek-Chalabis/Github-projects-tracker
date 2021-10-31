from api.utils_api import dictionary_compress


def test_dictionary_compress():
    tested_dict = {
        'test1': 1,
        'test2': 2,
        'test3': 3,
        'test4': 4,
    }
    compressed_dict = dictionary_compress(
        dictionary_to_compress=tested_dict,
        keys_to_keep={'test1', 'test3'},
    )
    assert compressed_dict == {'test1': 1, 'test3': 3}
