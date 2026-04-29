<?php

require_once __DIR__ . '/../vendor/autoload.php';
require_once __DIR__ . '/featuresDeclare.php';
require_once __DIR__ . '/NodeVisitor.php';


use PhpParser\ParserFactory;
use PhpParser\NodeTraverser;
use Features\featureWrapper;
use NodeVisitor\NodeVisitor;
use PhpParser\PhpVersion;

class astBuilder
{
    public $parser;

    public function __construct()
    {
        $factory = new ParserFactory();
        $this->parser = $factory->createForVersion(PhpParser\PhpVersion::fromString('5.6'));
    }

    public function builder($code)
    {
        
        $feature = new featureWrapper();
#debug
        $code = preg_replace('/\$(\w+)\{([^}]+)\}/', '$\1[\2]', $code);
        $code = str_replace(["<?PHP", "<?Php"], "<?php", $code);
        $code = str_replace('@', '', $code);

        try {
            $stmts = $this->parser->parse($code);
        } catch (\Throwable $e) {
            error_log("Parse error in code: " . $e->getMessage());
            return $feature->toArray();
        }

        $traverser = new NodeTraverser();
        $visitor = new NodeVisitor($feature);
        $traverser->addVisitor($visitor);
        $traverser->traverse($stmts);

        return $feature->toArray();
    }

}

?>