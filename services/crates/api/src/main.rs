use axum::{
    extract::{State, Json},
    routing::{get, post},
    Router,
    http::StatusCode,
    response::IntoResponse,
};
use std::net::SocketAddr;
use dotenvy::dotenv;
use sqlx::postgres::PgPoolOptions;
use tower_http::cors::{Any, CorsLayer};
use tracing::info;
use std::sync::Arc;

// Internal crate imports
use users_crate::{UserManager, models::{CreateUserRequest, LoginRequest}};

// Shared application state
struct AppState {
    db: sqlx::PgPool,
    graph: neo4rs::Graph,
    user_manager: UserManager,
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    // Load environment variables from .env
    dotenv().ok();

    // Initialize tracing/logging
    tracing_subscriber::fmt()
        .with_env_filter(tracing_subscriber::EnvFilter::from_default_env())
        .init();

    info!("Initializing SueChef Core API...");

    let db_url = std::env::var("DATABASE_URL")
        .expect("DATABASE_URL must be set in .env");
    
    let pool = PgPoolOptions::new()
        .max_connections(5)
        .connect(&db_url)
        .await?;

    info!("PostgreSQL connection pool established");

    let neo4j_url = std::env::var("NEO4J_URL").unwrap_or_else(|_| "bolt://localhost:7687".to_string());
    let neo4j_user = std::env::var("NEO4J_USER").unwrap_or_else(|_| "neo4j".to_string());
    let neo4j_pass = std::env::var("NEO4J_PASS").unwrap_or_else(|_| "password".to_string());

    let graph_config = neo4rs::ConfigBuilder::default()
        .uri(neo4j_url)
        .user(neo4j_user)
        .password(neo4j_pass)
        .build()?;

    let graph = neo4rs::Graph::connect(graph_config).await?;
    info!("Neo4j connection established");

    let jwt_secret = std::env::var("JWT_SECRET").expect("JWT_SECRET must be set in .env");
    let user_manager = UserManager::new(pool.clone(), jwt_secret);

    let state = Arc::new(AppState {
        db: pool,
        graph,
        user_manager,
    });

    let cors = CorsLayer::new()
        .allow_origin(Any)
        .allow_methods(Any)
        .allow_headers(Any);

    // Router setup
    let app = Router::new()
        // Health Check
        .route("/health", get(|| async { "OK" }))

        // Auth Routes
        .route("/api/v1/auth/register", post(register_handler))
        .route("/api/v1/auth/login", post(login_handler))

        // Basic Recipe Routes
        .route("/api/v1/recipes", get(get_recipes_handler))
        .route("/api/v1/recipes", post(create_recipe_handler))
        
        .layer(cors)
        .with_state(state);


    // Start Server
    let port = std::env::var("API_PORT").unwrap_or_else(|_| "8080".to_string());
    let addr = SocketAddr::V4(format!("0.0.0.0:{}", port).parse().unwrap());
    
    info!("SueChef API listening on {}", addr);
    let listener = tokio::net::TcpListener::bind(&addr).await.unwrap();
    axum::serve(listener, app).await?;

    Ok(())
}

// --- Handlers ---

async fn register_handler(
    State(state): State<Arc<AppState>>,
    Json(payload): Json<CreateUserRequest>,
) -> impl IntoResponse {
    match state.user_manager.register(payload).await {
        Ok(auth_response) => (StatusCode::OK, Json(auth_response)).into_response(),
        Err(err) => (StatusCode::BAD_REQUEST, Json(err)).into_response(),
    }
}

async fn login_handler(
    State(state): State<Arc<AppState>>,
    Json(payload): Json<LoginRequest>,
) -> impl IntoResponse {
    match state.user_manager.login(payload).await {
        Ok(auth_response) => (StatusCode::OK, Json(auth_response)).into_response(),
        Err(err) => (StatusCode::BAD_REQUEST, Json(err)).into_response(),
    }
}


async fn get_recipes_handler() -> &'static str {
    "Get Recipes Handler"
}

async fn create_recipe_handler() -> &'static str {
    "Create Recipe Handler"
}