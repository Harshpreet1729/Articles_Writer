# WriteYourOwn

<p align="center">
  <img src="templates/svgs/magnifier.svg" alt="WriteYourOwn icon" width="54">
</p>

WriteYourOwn is a Django writing platform built around one clear loop: authenticate, write, organize, measure, and ship content. The project uses a custom email-first user model, article ownership rules, automatic word counting, search, and production-friendly deployment settings.

## Workflow-First Overview

```mermaid
flowchart LR
    A[Visitor lands on site] --> B[Signup page at /]
    B --> C[Allauth authentication]
    C --> D[User account created with email as login]
    D --> E[Redirect to article workspace]
    E --> F[Create article]
    E --> G[Search personal articles]
    E --> H[Update owned article]
    E --> I[Delete owned article]
    F --> J[Word count auto-calculated]
    H --> J
    J --> K[Dashboard reflects article count + total written words]
```

WriteYourOwn is designed as a personal writing workspace, not a public publishing feed. Every major flow is centered on the authenticated user and their own article set.

## Application Workflow

```mermaid
flowchart TD
    A[Browser Request] --> B{Requested URL}
    B -->|/| C[SignupView]
    B -->|/accounts/*| D[django-allauth routes]
    B -->|/articles/| E[ArticleListView]
    B -->|/articles/create/| F[ArticleCreateView]
    B -->|/articles/<pk>/update/| G[ArticleUpdateView]
    B -->|/articles/<pk>/delete/| H[ArticleDeleteView]
    B -->|/<ADMIN_URL>/| I[Django Admin]

    C --> J[Create or authenticate user]
    D --> J
    E --> K[Filter by request.user]
    F --> L[Attach creator before save]
    G --> M[Allow only owner]
    H --> N[Allow only owner + success message]
```

The routing strategy is intentionally simple: authentication is front-loaded, article actions live under `/articles/`, and the admin path is environment-controlled through `ADMIN_URL`.

## Authentication and Access Control Workflow

```mermaid
flowchart TD
    A[User enters email credentials] --> B[allauth backend]
    B --> C[Custom UserProfile model]
    C --> D[USERNAME_FIELD = email]
    D --> E[Successful login]
    E --> F[LOGIN_REDIRECT_URL = home]

    G[Anonymous request to article page] --> H[LoginRequiredMixin]
    H --> I[Redirect to login flow]

    J[Update/Delete request] --> K[UserPassesTestMixin]
    K --> L{request.user == article.creator}
    L -->|Yes| M[Allow edit or delete]
    L -->|No| N[Reject access]
```

Theory: the project combines `django-allauth` with a custom `AbstractUser` extension so email becomes the primary identity. Authorization is then enforced at the view layer, especially for update and delete actions.

## Article Lifecycle Workflow

```mermaid
flowchart LR
    A[Writer opens create form] --> B[Enter title, status, content, twitter_post]
    B --> C[Submit CreateView]
    C --> D[creator = current user]
    D --> E[Article save method]
    E --> F[Strip HTML-like tags from content]
    F --> G[Count words with regex]
    G --> H[Persist article]
    H --> I[Redirect to article list]
    I --> J[Paginated personal dashboard]
```

```mermaid
flowchart LR
    A[Existing article] --> B[Update form]
    B --> C[Ownership check]
    C --> D[Save updated content]
    D --> E[Recompute word count]
    E --> F[Refresh article list]
```

```mermaid
flowchart LR
    A[Delete request] --> B[Ownership check]
    B --> C[DeleteView POST]
    C --> D[Success message: article deleted]
    D --> E[Redirect back to home]
```

Theory: the article model is optimized for a writer's working draft cycle. Status tracks writing progress, and `word_count` is derived automatically so metrics stay consistent without manual input.

## Search and Dashboard Workflow

```mermaid
flowchart TD
    A[User opens article list] --> B[ListView get_queryset]
    B --> C[Base queryset = articles by current user]
    C --> D{search query present?}
    D -->|No| E[Order by created_at descending]
    D -->|Yes| F[Apply title__search filter]
    F --> E
    E --> G[Paginate by 5]
    G --> H[Render home template]

    I[Dashboard metrics] --> J[Count owned articles]
    I --> K[Sum stored word counts]
    J --> L[article_count property]
    K --> M[written_words property]
```

Theory: the dashboard is private by design. Search only inspects the current user's articles, and model properties expose lightweight productivity metrics directly from relational data.

## Configuration Workflow

```mermaid
flowchart TD
    A[Environment variables] --> B[_env helpers normalize values]
    B --> C[Core runtime settings]
    C --> D[DEBUG]
    C --> E[SECRET_KEY]
    C --> F[DATABASE_URL]
    C --> G[ALLOWED_HOSTS]
    C --> H[CSRF_TRUSTED_ORIGINS]
    C --> I[ADMIN_URL]

    F --> J[dj_database_url.parse]
    J --> K{PostgreSQL?}
    K -->|Yes| L[Add connect_timeout]
    K -->|No| M[Use SQLite/local DB]

    A --> N[ENV_STATE]
    N --> O{production?}
    O -->|Yes| P[Secure cookies + proxy SSL headers]
    O -->|No| Q[Local-friendly defaults]
```

Theory: settings are built around environment-first deployment. Local development stays fast, while production enables stricter cookie, proxy, and host handling without needing a separate settings module.

## Email Delivery Workflow

```mermaid
flowchart LR
    A[ENV_STATE + EMAIL_PROVIDER] --> B{Provider selected}
    B -->|mailjet| C[Read Mailjet credentials]
    B -->|mailgun| D[Read Mailgun credentials]
    B -->|other/fallback| E[Use configured backend or console]

    C --> F{Credentials present?}
    D --> G{API key present?}
    F -->|Yes| H[Anymail Mailjet backend]
    F -->|No| I[Console backend + warning]
    G -->|Yes| J[Anymail Mailgun backend]
    G -->|No| K[Console backend + warning]
```

Theory: the email setup is failure-aware. If production credentials are incomplete, the app falls back to console email instead of crashing silently, making misconfiguration easier to spot.

## Delivery Workflow

```mermaid
flowchart TD
    A[Developer change] --> B{Run mode}
    B -->|Poetry| C[Install dependencies]
    B -->|Docker| D[Build containers]

    C --> E[Set env vars]
    D --> E
    E --> F[Run migrations]
    F --> G[Start Django app]
    G --> H[Serve static assets]
    H --> I[Local usage or Railway deploy]

    I --> J{Railway production}
    J -->|Yes| K[Set DATABASE_URL + ENV_STATE=production]
    K --> L[Configure ADMIN_URL and email provider]
    L --> M[Update Django Site domain]
```

## Project Map

```mermaid
flowchart TD
    A[Repository Root] --> B[app/]
    A --> C[djangoproject/]
    A --> D[templates/]
    A --> E[static/]
    A --> F[tests/]
    A --> G[Dockerfile]
    A --> H[docker-compose.yml]
    A --> I[start-django.sh]

    B --> B1[models.py]
    B --> B2[views.py]
    B --> B3[urls.py]
    C --> C1[settings.py]
    C --> C2[urls.py]
    F --> F1[pytest tests]
    F --> F2[Playwright page flows]
```

## Quick Start

### Poetry path

```bash
git clone https://github.com/Harshpreet1729/WriteYourOwn.git
cd WriteYourOwn
poetry install
poetry run python manage.py migrate
poetry run python manage.py runserver
```

### Docker path

```bash
docker compose up --build
```

App URL: `http://127.0.0.1:8000`

## Minimum Environment Variables

```env
ENV_STATE=dev
DEBUG=True
SECRET_KEY=change-me
DATABASE_URL=sqlite:///db.sqlite3
ALLOWED_HOSTS=127.0.0.1,localhost
ADMIN_URL=admin
```

## Test Workflow

```mermaid
flowchart LR
    A[Developer runs tests] --> B[pytest suite]
    B --> C[Homepage checks]
    B --> D[Signup checks]
    B --> E[Playwright-assisted flows]
```

Run:

```bash
poetry run pytest
```

Install Playwright browsers if needed:

```bash
poetry run playwright install --with-deps
```

## Common Notes

- Search uses PostgreSQL full-text search on article titles.
- Static files are served with WhiteNoise.
- The admin URL is intentionally customizable.
- Production uses secure cookie and proxy-aware settings when `ENV_STATE=production`.

## Author

Harshpreet1729
