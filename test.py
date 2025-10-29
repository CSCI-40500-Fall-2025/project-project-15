import pytest
import os
import tempfile
import shutil
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
from prototype import count_files, parse_commit

class TestParseCommit:
    '''
    Test class for parse_commit function
    Tests the parsing of git commit messages into type and content
    '''
    
    # Test parsing a commit with conventional commit format (type: message)
    def test_parse_commit_with_conventional_format(self):
        result = parse_commit("feat: add new feature")
        assert result["type"] == "feat"
        assert result["content"] == "add new feature"
    
    # Test parsing a commit without specific type of prefix
    def test_parse_commit_without_type(self):
        result = parse_commit("just a regular commit message")
        assert result["type"] == "other"
        assert result["content"] == "just a regular commit message"
    
    # Test for removal of trailing white spaces
    def test_parse_commit_with_whitespace(self):
        result = parse_commit("fix:   resolve bug with spaces  ")
        assert result["type"] == "fix"
        assert result["content"] == "resolve bug with spaces"
    
    # Testing messages with multiple colons, only remove one colon
    def test_parse_commit_with_multiple_colons(self):
        result = parse_commit("docs: update README: add installation section")
        assert result["type"] == "docs"
        assert result["content"] == "update README: add installation section"
    
    # Test empty string 
    def test_parse_commit_empty_string(self):
        result = parse_commit("")
        assert result["type"] == "other"
        assert result["content"] == ""

class TestCountFiles:
    """
    Test class for count_files function
    Tests file counting functionality with various directory structures
    """
    
    # Create test environment, bubble up with files + directories
    @pytest.fixture
    def test_project(self):
        temp_dir = tempfile.mkdtemp()
        
        # Create main files
        Path(temp_dir, "main.py").touch()
        Path(temp_dir, "README.md").touch()
        Path(temp_dir, ".hidden").touch()
        
        # Create subdirectory with files
        subdir = Path(temp_dir, "src")
        subdir.mkdir()
        Path(subdir, "app.py").touch()
        Path(subdir, "utils.py").touch()
        
        # Create excluded directories
        git_dir = Path(temp_dir, ".git")
        git_dir.mkdir()
        Path(git_dir, "config").touch()
        
        venv_dir = Path(temp_dir, "venv")
        venv_dir.mkdir()
        Path(venv_dir, "lib.py").touch()
        
        yield temp_dir
        shutil.rmtree(temp_dir)
    
    # test file counting (main.py, README.md, app.py, utils.py) expected 4
    def test_count_files_basic(self, test_project):
        count, dir_names = count_files(test_project)
        assert count == 4
        assert isinstance(dir_names, list)
    
    # test file counting, make sure it doesn't count hidden files
    # should only count hidden.py
    def test_count_files_excludes_hidden_files(self):
        """Test ONLY hidden file exclusion"""
        temp_dir = tempfile.mkdtemp()
        Path(temp_dir, "visible.py").touch()
        Path(temp_dir, ".hidden").touch()
        
        count, _ = count_files(temp_dir)
        assert count == 1
        
        shutil.rmtree(temp_dir)
    
    # test file counting, make sure .git directory not counted
    def test_count_files_excludes_git_directory(self):
        temp_dir = tempfile.mkdtemp()

        Path(temp_dir, "main.py").touch()

        # Create .git directory with files
        git_dir = Path(temp_dir, ".git")
        git_dir.mkdir()
        Path(git_dir, "config").touch()
        Path(git_dir, "HEAD").touch()
        
        count, dir_names = count_files(temp_dir)
        # Should only count main.py not .git folder
        assert count == 1
        
        # Verify .git files are not in the directory listing
        all_files = [item for sublist in dir_names for item in sublist]
        assert "config" not in all_files
        assert "HEAD" not in all_files
        
        shutil.rmtree(temp_dir)
    
    # test file counting, make sure venv directory not counted
    def test_count_files_excludes_venv_directory(self):
        temp_dir = tempfile.mkdtemp()
        Path(temp_dir, "main.py").touch()
        
        venv = Path(temp_dir, "venv")
        venv.mkdir()
        Path(venv, "lib.py").touch()
        
        count, _ = count_files(temp_dir)
        # only count lib.py
        assert count == 1 
        
        shutil.rmtree(temp_dir)
    
    # test file count on empty directory 
    def test_count_files_empty_directory(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            count, dir_names = count_files(temp_dir)
            assert count == 0

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])