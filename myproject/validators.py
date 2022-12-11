import re
from rest_framework import serializers

def alpha_only(value):
    slug_re = re.compile(r'^[-a-zA-Z_]+$')
    if not slug_re.match(value):
        raise serializers.ValidationError('Not an alphabet slug. Digits not allowed by fucntion validation')
    return value


class AlphaOnlyValidator:
    def __init__(self, var):
        self.some_internal_var = var

    def __call__(self, value):
        print(self.some_internal_var)
        slug_re = re.compile(r'^[-a-zA-Z_]+$')
        if not slug_re.match(value):
            raise serializers.ValidationError('Not an alphabet slug. Digits not allowed by class validation')
        return value
