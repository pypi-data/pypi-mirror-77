import setuptools
from pathlib import Path

setuptools.setup(
  name="Pygkquiz",
  version=1.1,
  long_description=Path("README.md").read_text(),
  author= "Ashok Kumar",
  author_email= "ashbhati2@gmail.com",
  packages=setuptools.find_packages(exclude=["tests","data"])
)
