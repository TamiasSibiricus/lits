from rest_access_policy import AccessPolicy


class AdminOnlyAccessPolicy(AccessPolicy):
    statements = [
        {
            "action": ["*"],
            "principal": ["admin"],
            "effect": "allow"
        }
    ]


class ArticleAccessPolicy(AccessPolicy):
    statements = [
        {
            "action": ["list", "retrieve"],
            "principal": "*",
            "effect": "allow"
        },
        {
            "action": ["*"],
            "principal": ["admin", "group:editor", "group:admin"],
            "effect": "allow"
        }
    ]
