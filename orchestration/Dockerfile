FROM quay.io/astronomer/astro-runtime:11.0.0

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy dbt profiles
COPY transformation/profiles.yml /usr/local/airflow/dbt/profiles.yml
