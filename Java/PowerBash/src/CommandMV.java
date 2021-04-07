import java.util.ArrayList;

//Convert from path to a node in the filesystem. Check for errors. Let the filesystem move the node
class CommandMV extends Command {
    private ArrayList<String> arguments;

    CommandMV(ArrayList<String> arguments) {
        this.arguments = arguments;
    }

    public ResultCollector execute() {

        ResultCollector resultCollector = new ResultCollector();
        String pathSource;

        if (arguments.get(0).contains("/"))
            pathSource = arguments.get(0).substring(0, arguments.get(0).lastIndexOf("/"));
        else pathSource = "";

        String nameSource = arguments.get(0).substring(arguments.get(0).lastIndexOf("/") + 1);
        Node source = pathToNode(pathSource, arguments.get(0));

        if (source == null || !source.contains(nameSource))
            resultCollector.setError("mv: cannot move " + arguments.get(0) + ": No such file or directory");
        else {
            for (Node aux : source.getContent())
                if (aux.getDataName().equals(nameSource))
                    source = aux;

            Node destination = pathToNode(arguments.get(1), arguments.get(0));

            if (destination == null)
                resultCollector.setError("cp: cannot move into " + arguments.get(1) + ": No such directory");
            else if (destination.contains(nameSource))
                resultCollector.setError("cp: cannot move " + arguments.get(0) + ": Node exists at destination");
            else fileSystem.mv(source, destination);
        }
        return resultCollector;
    }
}
