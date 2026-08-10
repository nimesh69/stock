FROM node:20-alpine

WORKDIR /frontend

# Copy package configuration files
COPY package.json package-lock.json* /frontend/

# Install dependencies
RUN npm install

# Copy the rest of the application source code
COPY . /frontend/

EXPOSE 3000

# Start command (change to "npm run dev" if you are using Vite)
CMD ["npm", "start"]
