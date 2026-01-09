import reflex as rx


tailwind_config = {
    "plugins": ["@tailwindcss/typography"],
    "theme": {
        "extend": {
            "colors": {
                "background": "var(--background)",
                "foreground": "var(--foreground)",
            },
        }
    },
}

config = rx.Config(
    app_name="app",
    plugins=[
        #rx.plugins.TailwindV3Plugin(),
        #rx.plugins.TailwindV4Plugin(tailwind_config),
        rx.plugins.TailwindV4Plugin(),
    ],
    disable_plugins=[
        "reflex.plugins.sitemap.SitemapPlugin",
    ],
)

