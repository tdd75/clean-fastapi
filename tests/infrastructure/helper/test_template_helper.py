from typing import Generator

import pytest
from pathlib import Path
from tempfile import TemporaryDirectory
from jinja2 import Environment, FileSystemLoader
from faker import Faker

from app.infrastructure.helper.template_helper import render_template

fake = Faker()


@pytest.fixture
def fake_template_env() -> Generator[tuple[str, Path], None, None]:
    with TemporaryDirectory() as tmpdir:
        template_dir = Path(tmpdir)
        template_name = f'{fake.file_name(extension="html")}'
        template_path = template_dir / template_name
        template_path.write_text('Hello, {{ name }}!')
        yield template_name, template_dir


class TestRenderTemplate:
    def test_render_template_with_context(self, fake_template_env, monkeypatch):
        # Arrange
        template_name, template_dir = fake_template_env
        env = Environment(loader=FileSystemLoader(template_dir))
        monkeypatch.setattr('app.infrastructure.helper.template_helper.env', env)

        # Act
        name = fake.first_name()
        result = render_template(template_name, {'name': name})

        # Assert
        assert result == f'Hello, {name}!'

    def test_render_template_empty_context(self, fake_template_env, monkeypatch):
        template_name, template_dir = fake_template_env
        env = Environment(loader=FileSystemLoader(template_dir))
        monkeypatch.setattr('app.infrastructure.helper.template_helper.env', env)

        result = render_template(template_name)
        assert 'Hello, !' in result
