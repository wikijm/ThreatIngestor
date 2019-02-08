from jsonpath_rw import jsonpath, parse

import json

from threatingestor.sources import Source

class AbstractPlugin(Source):

    def __init__(self, name, paths, reference):
        """Args should be url, auth, etc, whatever is needed to set up the object.

        The name argument is required for all Source plugins, and is used internally.
        """
        self.name = name
        self.paths=paths
        self.reference= reference

    def get_content(self):
        """Return dict or list of raw content to process.

        Override in child class."""
        raise NotImplementedError()

    def run(self, saved_state):
        """Run and return (saved_state, list(Artifact))"""
        artifact_list = []
        for path in self.paths:
            jsonpath_expr = parse(path)
            matches = jsonpath_expr.find(self.get_content())

            for match in matches:
                artifact_list += self.process_element(match.value, self.reference, include_nonobfuscated=True)


        return saved_state, artifact_list
