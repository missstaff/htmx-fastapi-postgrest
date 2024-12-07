# Use the official PostgREST image
FROM postgrest/postgrest:latest

# Copy your PostgREST config into the container
COPY postgrest.conf ./postgrest.conf

# Expose the port PostgREST will run on
EXPOSE 3000

# Run PostgREST with the config file
CMD ["postgrest", "./postgrest.conf"]
