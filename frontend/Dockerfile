# Stage 1: Build the application
FROM node:22-alpine AS builder

# Set working directory
WORKDIR /app

# Copy package files and install dependencies
COPY package*.json ./
RUN npm install

# Copy the rest of the application code
COPY . .

# Build the Nuxt application
RUN npm run build

# Stage 2: Run the production application
FROM node:22-alpine AS runner

WORKDIR /app

# Copy the build output from the builder stage
COPY --from=builder /app/.output /app/.output

# Set environment variables
ENV HOST=0.0.0.0
ENV NODE_ENV=production
ENV PORT=3000

# Expose the port on which Nuxt listens (default is 3000)
EXPOSE 3000

# Healthcheck (optional but recommended)
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s \
  CMD wget --quiet --tries=1 --spider http://localhost:3000 || exit 1

# Start the Nuxt server
CMD ["node", ".output/server/index.mjs"]