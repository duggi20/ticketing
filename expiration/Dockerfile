FROM node:alpine

# Create app directory
WORKDIR /app

# Copy package metadata and install dependencies
COPY package.json .
RUN npm install --omit=dev

# Copy application source
COPY . .

# Default port and expose
ENV PORT=3000
EXPOSE 3000

# Run the application
CMD ["npm", "start"]
