import openwhisk from 'openwhisk'
import { readFile, rm, mkdir } from 'fs/promises'
import { createWriteStream } from 'fs'

const options = {
    apihost: '127.0.0.1:31001', 
    api_key: '23bc46b1-71f6-4ed5-8c54-816aa4f8c502:123zO3xZCLrMN6v2BKK1dXYFpXlPkccOFqm12CdAsMgRU4VrNZ9lyGVCGuMDGIwP',
    ignore_certs: true
}
const ow = openwhisk(options)

let depth = 1
let parallelism = 4
let iterations = 1
let outputFile = null
async function read_args() {
    console.log("Read arguments:")
    console.log(process.argv)
    depth = parseInt(process.argv[2])
    parallelism = parseInt(process.argv[3])
    iterations = parseInt(process.argv[4])
    const outputFilename = `results_depth-${depth}_parallelism-${parallelism}_iters-${iterations}.csv`
    const outputLocation = process.argv[5] ? process.argv[5]:"."
    await mkdir(outputLocation, {recursive: true})
    outputFile = createWriteStream(outputLocation+"/"+outputFilename, {flush: true})
}

async function setup() {
    let createdActions = []
    const actionFile = await readFile("hello.js", {encoding: "utf8"})

    // await ow.actions.delete({name: "seq1"}, )
    for (let i=0;i<depth;i++) {
        const actionName = `hello${i}`
        // await ow.actions.delete({name: actionName})
        await ow.actions.create({
            name: actionName,
            overwrite: true,
            kind: "nodejs:12",
            action: actionFile
        })
        createdActions.push(actionName)
    }

    // console.log(createdActions)
    await ow.actions.create({
        name: "seq1",
        overwrite: true,
        sequence: createdActions.map((n) => "/guest/"+n)
    })
    console.log("Created sequence")
}

async function run_exp() {
    const invocations = []
    const promises = []
    for(let i=0;i<parallelism;i++) {
        const promise = ow.actions.invoke("seq1")
        const start = Date.now()
        invocations.push({
            start: start
        })
        const chain = promise.then((result) => {
            invocations[i].end = Date.now()
            return result
        })
        promises.push(chain)
    }
    const result = await Promise.all(promises)
    for (const invocation of invocations) {
        outputFile.write(`${invocation["start"]},${invocation["end"]}\n`)
    }
    // console.log(invocations)
}

read_args()
for (let i=0;i<iterations;i++) {
    await setup()
    await run_exp()
}
outputFile.end()
