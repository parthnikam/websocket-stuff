/// <reference path="../pb_data/types.d.ts" />
migrate((app) => {
  const collection = app.findCollectionByNameOrId("pbc_493096279")

  // update collection data
  unmarshal({
    "indexes": [
      "CREATE INDEX `idx_MJbJcmJEV9` ON `all_messages` (`roomId`)"
    ]
  }, collection)

  return app.save(collection)
}, (app) => {
  const collection = app.findCollectionByNameOrId("pbc_493096279")

  // update collection data
  unmarshal({
    "indexes": []
  }, collection)

  return app.save(collection)
})
