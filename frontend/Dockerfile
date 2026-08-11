FROM node:20-alpine

WORKDIR /frontend

# Copy package configuration files
COPY package.json package-lock.json* /frontend/

# Install dependencies
RUN npm install

# Copy the rest of the application source code
COPY . /frontend/

# Match Vite's default dev port
EXPOSE 5173

# Run the Vite development server accessible from outside the container
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]