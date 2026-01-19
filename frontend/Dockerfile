FROM node:24-slim AS base
COPY . /app
WORKDIR /app

FROM base AS build
RUN --mount=type=cache,id=npm,target=/npm/store npm install --frozen-lockfile
RUN npm run build

FROM base
COPY --from=build /app/node_modules /app/node_modules
COPY --from=build /app/.next /app/.next
EXPOSE 3000
CMD [ "npm", "start" ]
