import logging
import os
import shutil
import tempfile
import uuid
from pathlib import Path
from typing import Tuple, List, Text, Set, Union, Optional, Iterable

from rasa.constants import DEFAULT_E2E_TESTS_PATH
from rasa.nlu.training_data import loading as nlu_loading

logger = logging.getLogger(__name__)

MARKDOWN_FILE_EXTENSIONS = {".md"}

YAML_FILE_EXTENSIONS = {".yml", ".yaml"}

JSON_FILE_EXTENSIONS = {".json"}

TRAINING_DATA_EXTENSIONS = JSON_FILE_EXTENSIONS.union(MARKDOWN_FILE_EXTENSIONS).union(
    YAML_FILE_EXTENSIONS
)


def get_core_directory(paths: Optional[Union[Text, List[Text]]],) -> Text:
    """Recursively collects all Core training files from a list of paths.

    Args:
        paths: List of paths to training files or folders containing them.

    Returns:
        Path to temporary directory containing all found Core training files.
    """
    core_files, _ = get_core_nlu_files(paths)
    return _copy_files_to_new_dir(core_files)


def get_nlu_directory(paths: Optional[Union[Text, List[Text]]],) -> Text:
    """Recursively collects all NLU training files from a list of paths.

    Args:
        paths: List of paths to training files or folders containing them.

    Returns:
        Path to temporary directory containing all found NLU training files.
    """
    _, nlu_files = get_core_nlu_files(paths)
    return _copy_files_to_new_dir(nlu_files)


def get_core_nlu_directories(
    paths: Optional[Union[Text, List[Text]]],
) -> Tuple[Text, Text]:
    """Recursively collects all training files from a list of paths.

    Args:
        paths: List of paths to training files or folders containing them.

    Returns:
        Path to directory containing the Core files and path to directory
        containing the NLU training files.
    """

    story_files, nlu_data_files = get_core_nlu_files(paths)

    story_directory = _copy_files_to_new_dir(story_files)
    nlu_directory = _copy_files_to_new_dir(nlu_data_files)

    return story_directory, nlu_directory


def get_core_nlu_files(
    paths: Optional[Union[Text, List[Text]]]
) -> Tuple[List[Text], List[Text]]:
    """Recursively collects all training files from a list of paths.

    Args:
        paths: List of paths to training files or folders containing them.

    Returns:
        Tuple of paths to story and NLU files.
    """

    story_files = set()
    nlu_data_files = set()

    if paths is None:
        paths = []
    elif isinstance(paths, str):
        paths = [paths]

    for path in set(paths):
        if not path:
            continue

        if _is_valid_filetype(path):
            if is_nlu_file(path):
                nlu_data_files.add(os.path.abspath(path))
            elif is_story_file(path):
                story_files.add(os.path.abspath(path))
        else:
            new_story_files, new_nlu_data_files = _find_core_nlu_files_in_directory(
                path
            )

            story_files.update(new_story_files)
            nlu_data_files.update(new_nlu_data_files)

    return sorted(story_files), sorted(nlu_data_files)


def _find_core_nlu_files_in_directory(directory: Text,) -> Tuple[Set[Text], Set[Text]]:
    story_files = set()
    nlu_data_files = set()

    for root, _, files in os.walk(directory, followlinks=True):
        # we sort the files here to ensure consistent order for repeatable training
        # results
        for f in sorted(files):
            full_path = os.path.join(root, f)

            if not _is_valid_filetype(full_path):
                continue

            if is_nlu_file(full_path):
                nlu_data_files.add(full_path)
            elif is_story_file(full_path):
                story_files.add(full_path)

    return story_files, nlu_data_files


def _is_valid_filetype(path: Text) -> bool:
    return os.path.isfile(path) and Path(path).suffix in TRAINING_DATA_EXTENSIONS


def is_nlu_file(file_path: Text) -> bool:
    """Checks if a file is a Rasa compatible nlu file.

    Args:
        file_path: Path of the file which should be checked.

    Returns:
        `True` if it's a nlu file, otherwise `False`.
    """
    return nlu_loading.guess_format(file_path) != nlu_loading.UNK


def is_story_file(file_path: Text) -> bool:
    """Checks if a file is a Rasa story file.

    Args:
        file_path: Path of the file which should be checked.

    Returns:
        `True` if it's a story file, otherwise `False`.
    """
    from rasa.core.training.story_reader.yaml_story_reader import YAMLStoryReader

    if YAMLStoryReader.is_yaml_story_file(file_path):
        return True

    from rasa.core.training.story_reader.markdown_story_reader import (
        MarkdownStoryReader,
    )

    return MarkdownStoryReader.is_markdown_story_file(file_path)


def is_end_to_end_conversation_test_file(file_path: Text) -> bool:
    """Checks if a file is an end-to-end conversation test file.

    Args:
        file_path: Path of the file which should be checked.

    Returns:
        `True` if it's a conversation test file, otherwise `False`.
    """

    if Path(file_path).suffix not in MARKDOWN_FILE_EXTENSIONS:
        return False

    dirname = os.path.dirname(file_path)
    return (
        DEFAULT_E2E_TESTS_PATH in dirname
        and is_story_file(file_path)
        and not is_nlu_file(file_path)
    )


def is_config_file(file_path: Text) -> bool:
    """Checks whether the given file path is a Rasa config file.

       Args:
           file_path: Path of the file which should be checked.

       Returns:
           `True` if it's a Rasa config file, otherwise `False`.
       """

    file_name = os.path.basename(file_path)

    return file_name in ["config.yml", "config.yaml"]


def _copy_files_to_new_dir(files: Iterable[Text]) -> Text:
    directory = tempfile.mkdtemp()
    for f in files:
        # makes sure files do not overwrite each other, hence the prefix
        unique_prefix = uuid.uuid4().hex
        unique_file_name = unique_prefix + "_" + os.path.basename(f)
        shutil.copy2(f, os.path.join(directory, unique_file_name))

    return directory
