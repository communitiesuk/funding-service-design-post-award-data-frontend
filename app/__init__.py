from flask import Flask, render_template, request
from flask_assets import Environment
from flask_talisman import Talisman
from flask_wtf.csrf import CSRFProtect
from fsd_utils import init_sentry
from fsd_utils.healthchecks.checkers import FlaskRunningChecker
from fsd_utils.healthchecks.healthcheck import Healthcheck
from fsd_utils.logging import logging
from govuk_frontend_wtf.main import WTFormsHelpers
from jinja2 import ChoiceLoader, PackageLoader, PrefixLoader

import static_assets
from config import Config

assets = Environment()
talisman = Talisman()
csrf = CSRFProtect()


def create_app(config_class=Config):
    init_sentry()
    app = Flask(__name__, static_url_path="/static")
    csrf.init_app(app)
    app.config.from_object(config_class)
    logging.init_app(app)
    app.jinja_env.lstrip_blocks = True
    app.jinja_env.trim_blocks = True
    app.jinja_loader = ChoiceLoader(
        [
            PackageLoader("app"),
            PrefixLoader(
                {
                    "govuk_frontend_jinja": PackageLoader("govuk_frontend_jinja"),
                    "govuk_frontend_wtf": PackageLoader("govuk_frontend_wtf"),
                }
            ),
        ]
    )

    # Set content security policy
    csp = {
        "default-src": "'self'",
        "script-src": [
            "'self'",
            "'sha256-+6WnXIl4mbFTCARd8N3COQmT3bJJmo32N8q8ZSQAIcU='",
            "'sha256-l1eTVSK8DTnK8+yloud7wZUqFrI0atVo6VlC6PJvYaQ='",
        ],
    }

    @app.before_request
    def maintenance_page() -> str | None:
        if request.endpoint != "static" and app.config["MAINTENANCE_MODE"]:
            return render_template(
                "main/maintenance-mode.html", maintenance_ends_from=app.config["MAINTENANCE_ENDS_FROM"]
            )

        return None

    # Initialise app extensions
    app.static_folder = "static/dist/"
    assets.init_app(app)

    static_assets.init_assets(app, auto_build=Config.AUTO_BUILD_ASSETS, static_folder="static/dist")

    talisman.init_app(app, content_security_policy=csp, force_https=False)
    WTFormsHelpers(app)

    # Register blueprints
    from app.main import bp as main_bp

    app.register_blueprint(main_bp)

    health = Healthcheck(app)
    health.add_check(FlaskRunningChecker())

    return app


app = create_app()
