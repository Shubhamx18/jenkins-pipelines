# Use a JDK base image so 'javac' is available
FROM eclipse-temurin:17-jdk-alpine

# Set the working directory inside the container
WORKDIR /app

# Copy all project files into the container
COPY . .

# Compile app.java
RUN javac app.java

# Run the compiled Java application
CMD ["java", "app"]
